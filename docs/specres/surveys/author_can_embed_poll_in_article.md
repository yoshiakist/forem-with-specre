---
id: "01KJ2HPD31V6W1Y18QXE0RYG56"
name: "author_can_embed_poll_in_article"
status: "draft"
---

## Related Files

- `app/liquid_tags/poll_tag.rb`
- `app/views/liquids/_poll.html.erb` (Template)
- `app/assets/stylesheets/ltags/PollTag.scss` (Stylesheet)
- `spec/liquid_tags/poll_tag_spec.rb` (Test)

## Functional Overview

An admin can embed a standalone poll inside article content using the `{% poll <id> %}` Liquid tag. When the article is rendered, `PollTag` looks up the `Poll` record by its numeric ID and renders the `liquids/poll` partial, which outputs an interactive voting UI. The tag also injects an inline JavaScript block (`PollTag::SCRIPT`) that drives client-side voting behavior: it fetches the current user's vote state via `GET /poll_votes/:poll_id`, and — depending on whether the user has already voted — either displays the results distribution or attaches click handlers to the poll options. Signed-in users can cast a vote (`POST /poll_votes`) or skip to see results (`POST /poll_skips`). Signed-out users are prompted to log in when they interact with the poll.

## Design Intent

The poll is rendered entirely server-side as HTML plus a self-contained `<script>` block, avoiding any dependency on a JavaScript bundler or Stimulus controller. This ensures the poll works when embedded in article Markdown processed by the Liquid pipeline, where external JS imports are not available. The tag is restricted to admin and super-admin roles via `VALID_ROLES` and `user_authorization_method_name`, preventing non-admin authors from inserting polls.

## Key Members

- `PollTag::PARTIAL` — `"liquids/poll"`, the ERB partial that renders the poll HTML
- `PollTag::VALID_CONTEXTS` — `["Article"]`, restricting the tag to article bodies only
- `PollTag::VALID_ROLES` — `[:admin, :super_admin]`, restricting usage to admins
- `PollTag::SCRIPT` — inline JavaScript that handles vote fetching, casting, skipping, and result display
- `displayPollResults(json)` — JS function that replaces option labels with percentage bars based on voting distribution
- `submitMultipleChoiceVotes(pollId, csrfToken)` — JS function that collects all checked options and submits them sequentially for multiple-choice polls

## Scenarios

### Rendering a single-choice poll in an article

1. An admin writes `{% poll 42 %}` in an article body.
2. During Liquid rendering, `PollTag#initialize` calls `Poll.find(42)` to load the poll.
3. `PollTag#render` renders the `liquids/poll` partial, producing a `<div class="ltag-poll">` with radio-button options and a "Show Results" button.
4. When a signed-in reader views the article, the injected script calls `GET /poll_votes/42`.
5. If the user has not voted, click handlers are attached to each option; clicking one sends `POST /poll_votes` with the selected `poll_option_id`.
6. After a successful vote, `displayPollResults` replaces the options with percentage bars showing the vote distribution.

### Rendering a multiple-choice poll

1. An admin embeds a poll of type `multiple_choice`.
2. The partial renders checkbox inputs instead of radio buttons.
3. When the user clicks an option, the script toggles the checkbox and calls `submitMultipleChoiceVotes`, which iterates all checked options and sends a `POST /poll_votes` for each.
4. After all votes resolve, `displayPollResults` is called with the final voting data.

### Rendering a scale poll

1. An admin embeds a poll of type `scale`.
2. The partial sorts options numerically by their markdown value and renders them as radio buttons.
3. If the poll has exactly 5 options, the CSS class `scale-horizontal scale-5-options` is applied; for more than 5, `scale-horizontal scale-many-options` is used.
4. Voting behavior follows the single-choice path.

### Viewing results without voting (skip)

1. A signed-in user clicks the "Show Results" button instead of an option.
2. The script sends `POST /poll_skips` with the `poll_id`.
3. The response includes voting distribution data, which `displayPollResults` uses to render the result bars.

### Unauthenticated user interaction

1. A visitor who is not signed in clicks on the poll.
2. The script detects the absence of the `user-signed-in` meta tag and calls `showLoginModal()` to prompt login.

## Failures / Exceptions

- If the poll ID does not exist, `Poll.find(id_code)` in `PollTag#initialize` raises `ActiveRecord::RecordNotFound`, which Liquid surfaces as a tag rendering error.
- If the CSRF token meta tag is missing from the page when a user attempts to vote, the script shows an alert ("Whoops. There was an error. Your vote was not counted. Try refreshing the page.") and aborts the vote submission.
