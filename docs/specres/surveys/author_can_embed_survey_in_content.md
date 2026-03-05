---
id: "01KJ2HPDKS93VFBHHN6KXPZXH3"
name: "author_can_embed_survey_in_content"
status: "draft"
---

## Related Files

- `app/liquid_tags/survey_tag.rb`
- `app/views/liquids/_survey.html.erb` (Template)
- `app/views/liquids/_survey_poll.html.erb` (Template)
- `app/assets/stylesheets/ltags/SurveyTag.scss` (Stylesheet)
- `spec/liquid_tags/survey_tag_spec.rb` (Test)

## Functional Overview

An admin can embed a multi-poll survey into article or billboard content using the `{% survey <id> %}` Liquid tag. When rendered, `SurveyTag` loads the `Survey` with its polls and poll options (eager-loaded to avoid N+1 queries) and renders the `liquids/survey` partial, which outputs a paginated wizard UI: one poll is displayed at a time with Previous/Next navigation buttons and a progress indicator ("Question N of M"). The tag injects a self-contained JavaScript block (`SurveyTag::SCRIPT`) that handles all client-side interaction. For signed-in users, the script fetches the user's vote state via `GET /surveys/:id/votes`, hydrates any previously answered polls, and submits responses (votes, text inputs) via `POST /poll_votes` or `POST /polls/:id/poll_text_responses` as the user navigates forward. Each submission carries a `session_start` identifier for session-scoped tracking. For signed-out users, any interaction triggers the login modal. When all polls are answered and the user clicks "Finish," the polls container is hidden and a completion message is displayed.

## Design Intent

Unlike the standalone `PollTag` which renders one poll at a time and submits votes immediately on click, `SurveyTag` accumulates answers in a `pendingVotes` map and submits them only when the user navigates to the next question or finishes the survey. This deferred-submission pattern avoids partial saves if the user abandons the survey mid-way, and ensures that `SurveyCompletionService` fires only after deliberate progression. The `VALID_CONTEXTS` includes `Article`, `Billboard`, and `NilClass`, and the authorization checks are overridden to allow usage in arbitrary contexts (e.g., billboard rendering) without requiring the standard per-article context validation. A random `session_start` (0–999999) is generated client-side for each page load to scope this attempt's votes.

## Key Members

- `SurveyTag::VALID_CONTEXTS` — `["Article", "Billboard", "NilClass"]`, extending embedding beyond articles
- `SurveyTag.valid_context?(context)` — overrides base validation to allow nil source contexts
- `SurveyTag.user_authorized?(user)` — always returns true, bypassing role restrictions
- `SurveyTag::SCRIPT` — inline JavaScript implementing the multi-step wizard, vote hydration, deferred submission, and completion display
- `pendingVotes` — JS object keyed by `pollId`, storing the user's selections until submission
- `currentSession` — random integer generated per page load, passed as `session_start` on every vote/text submission
- `updateUI()` — JS function that shows the current poll, updates progress text, and enables/disables navigation buttons based on answered state

## Scenarios

### Embedding and rendering a survey in an article

1. An admin writes `{% survey 7 %}` in an article body.
2. `SurveyTag#initialize` loads `Survey.includes(polls: :poll_options).find(7)`.
3. The `liquids/survey` partial renders: a title, a polls container with each poll rendered via the `liquids/survey_poll` sub-partial (all hidden except the first via `style="display: none;"`), navigation buttons (Previous disabled, Next disabled), and a hidden completion message.
4. The injected script calls `updateUI()` immediately to set the progress text and show the first poll.

### Signed-in user completes a fresh survey (no prior responses)

1. The script fetches `GET /surveys/7/votes`; the response has `completed: false`, `can_submit: true`, and an empty `votes` map.
2. The user selects an option on the first poll; `handleSelection` stores the choice in `pendingVotes` and marks the poll as answered, enabling the Next button.
3. The user clicks Next; `submitPendingVotes` sends `POST /poll_votes` with the selected `poll_option_id` and `session_start`, then advances to the next poll.
4. Steps repeat for each poll. On the last poll, the Next button text changes to "Finish."
5. The user clicks Finish; pending votes are submitted, the polls container is hidden, and the completion message is displayed.

### Signed-in user resumes a partially completed survey

1. The script fetches `GET /surveys/7/votes`; the response returns previously answered polls in the `votes` map.
2. `setAndLockAnsweredPoll` marks each previously answered poll as answered and disables its options.
3. `currentPollIndex` is set to the first unanswered poll.
4. The user continues from where they left off.

### Resubmission survey (allow_resubmission is true)

1. The script fetches `GET /surveys/7/votes`; the response has `allow_resubmission: true`.
2. Regardless of prior completion, all polls are reset to unanswered state (options cleared, textareas emptied).
3. `currentPollIndex` is set to 0 and a fresh `currentSession` is used.
4. The user answers all polls from the beginning.

### Completed non-resubmission survey

1. The script fetches `GET /surveys/7/votes`; `completed: true` and `allow_resubmission: false`.
2. The polls container and navigation are hidden immediately; the completion message is displayed.

### Text input poll

1. A poll of type `text_input` renders a `<textarea>` instead of option buttons.
2. As the user types, `handleTextInput` stores `{ type: 'text', content: ... }` in `pendingVotes`.
3. On navigation, `submitPendingVotes` sends `POST /polls/:id/poll_text_responses` with `text_content` and `session_start`.

### Signed-out user interaction

1. A visitor clicks anywhere on the survey.
2. The script intercepts the click, calls `e.preventDefault()`, and invokes `showLoginModal()` if available.

## Failures / Exceptions

- If the survey ID does not exist, `Survey.find(id_code)` raises `ActiveRecord::RecordNotFound` during Liquid rendering.
- If `GET /surveys/:id/votes` fails (non-OK response), the script logs the error to the console and falls back to a fresh start — event listeners are still attached so the user can interact.
- If any `POST` request in `submitPendingVotes` fails, the script shows an alert ("There was a problem saving your votes. Please try again.") and prevents navigation to the next poll.
