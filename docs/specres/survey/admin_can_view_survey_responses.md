---
id: "01KHZMJ8FDAFEW4W3NYSVRQ3CQ"
name: "admin_can_view_survey_responses"
status: "draft"
---

## Related Files

- `app/controllers/admin/surveys_controller.rb`
- `app/views/admin/surveys/index.html.erb` (Template)
- `app/views/admin/surveys/show.html.erb` (Template)
- `spec/requests/admin/surveys_spec.rb` (Test)

## Functional Overview

Administrators can browse and inspect survey responses through two views. The index view lists all surveys in reverse chronological order, paginated at 25 per page, showing each survey's title, active status badge, poll count, and creation date. The detail view loads a single survey with its polls and poll options and computes a statistics summary — total completions, unique respondents, poll vote count, poll skip count, text response count, and the timestamp of the last completion — which is presented alongside the ordered list of polls and their options.

## Design Intent

Aggregating all response statistics in the controller's `show` action keeps the template free of query logic and allows the statistics hash to be a single, testable unit. Using `Survey.includes(polls: :poll_options)` in the `show` action avoids N+1 queries when rendering poll option lists in the template.

## Key Members

- `@surveys` — paginated, descending-by-creation `Survey` relation used by the index view
- `@survey` — a `Survey` loaded with `polls` and `poll_options` eagerly included
- `@survey_stats` — hash of aggregated statistics: `polls_count`, `completions_count`, `unique_respondents_count`, `poll_votes_count`, `poll_skips_count`, `poll_text_responses_count`, `last_completed_at`

## Scenarios

### Admin views the survey list

1. Admin navigates to the admin surveys index page.
2. The system loads all surveys ordered by creation date descending, paginated at 25 per page.
3. The page displays each survey as a table row with its title (linked to the detail page), an active/inactive badge, the number of polls, and the creation date.
4. When there are no surveys, the page shows an empty-state message instead of the table.

### Admin views survey details with statistics

1. Admin clicks a survey title from the index list.
2. The system loads the survey along with its polls and poll options, then computes response statistics by querying `survey_completions` and `PollTextResponse`.
3. The detail page displays the survey's title, active/inactive badge, and optional "Title Displayed" and "Allows Resubmission" badges.
4. A statistics panel shows total completions, unique respondents, number of polls, total poll votes, total poll skips, total text responses, and the creation, last-updated, and last-completed timestamps.

### Admin inspects polls and their options on the detail page

1. The admin is on the survey detail page.
2. Each poll is listed in position order, showing its type label and prompt.
3. If the poll has options, each option's label text and optional supplementary text are displayed.
4. If the survey has no polls, the panel shows a "No polls added yet" message.

### Admin views a newly created survey with no responses

1. Admin navigates to the detail page of a survey that has no completions and no votes.
2. The statistics panel shows zeroes for completions, unique respondents, votes, skips, and text responses.
3. The "Last completed at" field displays "Never".
4. The polls section reflects whatever polls and options were defined at creation time.

## Failures / Exceptions

- If the requested survey ID does not exist, `Survey.includes(...).find(params[:id])` raises `ActiveRecord::RecordNotFound`, which the application's standard error handling translates into a 404 response.
