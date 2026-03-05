---
id: "01KHZM8WACKF3RJZT65WP2P2E9"
name: "admin_can_create_survey"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/surveys_controller.rb`
- `app/javascript/admin/controllers/admin_surveys_controller.js`
- `spec/requests/admin/surveys_spec.rb` (Test)
- `app/views/admin/surveys/new.html.erb` (Template)
- `app/views/admin/surveys/_form.html.erb` (Template)
- `app/views/admin/surveys/_poll_fields.html.erb` (Template)

## Functional Overview

An admin creates a survey by filling out a form that captures a title, boolean flags (active, display title, allow resubmission), daily email distribution count, and an optional email context paragraph, together with one or more nested polls. Each poll carries a question, a type (single choice, multiple choice, text input, or scale), a display position, and — depending on type — either explicit answer options or a numeric min/max range. The Stimulus controller (`admin-surveys`) drives the form dynamically: admins can add or remove polls and options without a page reload, and the visible sections per poll (options vs. scale configuration) update instantly whenever the poll type changes. On submission the controller persists everything via nested attributes; on success it redirects to the survey list with a confirmation flash, and on validation failure it re-renders the form in place with an inline error message.

## Key Members

- `survey_params` — strong-parameter allowlist covering `:title`, `:active`, `:display_title`, `:allow_resubmission`, `:daily_email_distributions`, `:extra_email_context_paragraph`, and nested `polls_attributes` (with nested `poll_options_attributes`).
- `polls_attributes` nested fields — each poll permits `:id`, `:prompt_markdown`, `:type_of`, `:position`, `:scale_min`, `:scale_max`, `:_destroy`.
- `poll_options_attributes` nested fields — each option permits `:id`, `:markdown`, `:supplementary_text`, `:position`, `:_destroy`.
- Stimulus targets: `pollContainer`, `pollTemplate`, `poll`, `optionsContainer` — used to locate DOM nodes for dynamic insertion and removal.
- Timestamp-based index (`new Date().getTime()`) — used as a unique key when rendering new poll or option rows client-side, preventing Rails nested-attribute key collisions.

## Scenarios

### Successful creation with choice-based polls

1. Admin navigates to the new survey page; the form initializes with one blank poll row already present.
2. Admin fills in the survey title and optionally toggles active status, display title, and allow-resubmission flags.
3. Admin optionally sets a daily email distribution count and an extra email context paragraph.
4. Admin enters a question prompt for the pre-built poll and selects a type of `single_choice` or `multiple_choice`; the options section becomes visible while the scale section stays hidden.
5. Admin adds one or more answer options (each with option text and optional supplementary text) using the "Add Option" button; existing options can be removed individually.
6. Admin clicks "+ Add Poll" to insert additional polls and repeats the configuration steps for each.
7. Admin submits the form; the server creates the Survey, associated Poll records, and PollOption records in a single transaction.
8. Admin is redirected to the survey list page and sees a "Survey has been created!" success flash.

### Successful creation with a scale poll

1. Admin adds a poll and changes its type to `scale`; the options section hides and the scale configuration section appears.
2. Admin enters a numeric minimum and maximum value (e.g. 1 and 3).
3. Admin submits the form; the server creates the Survey and the Poll, then auto-generates one PollOption per integer step between min and max.
4. Admin is redirected to the survey list with a success flash; the scale options exist as discrete choice records.

### Adding and removing polls dynamically

1. Admin clicks "+ Add Poll"; the Stimulus controller clones the hidden poll template, replaces `NEW_RECORD` placeholders with a timestamp-based index, and appends the new poll row to the container.
2. The newly inserted poll's type defaults to the first available option; section visibility is updated immediately.
3. Admin clicks "Remove Poll" on any poll row; if the poll is a new (unsaved) record it is removed from the DOM entirely, otherwise a hidden `_destroy` field is set to `1` and the row is visually hidden so Rails will delete it on save.

### Changing poll type updates visible sections

1. Admin changes a poll's type selector to `text_input`; both the options section and the scale section hide immediately.
2. Admin changes the type to `scale`; the scale configuration section appears and the options section hides.
3. Admin changes the type to `single_choice` or `multiple_choice`; the options section appears and the scale section hides.

### Validation failure on submission

1. Admin submits the form without a title (or with other invalid data).
2. The server does not create any records.
3. The new-survey form is re-rendered with an inline danger flash listing the validation errors (e.g. "Title can't be blank").

## Failures / Exceptions

- If the `pollTemplate` or `pollContainer` Stimulus targets are missing from the DOM when "Add Poll" is clicked, the controller logs an error and aborts without inserting anything.
- If the poll row cannot be located when "Remove Poll" is clicked (e.g. the button is outside a `[data-admin-surveys-target="poll"]` element), the action silently returns without effect.
- On save failure, `@survey.errors_as_sentence` is written to `flash.now[:danger]` and the `:new` template is rendered (HTTP 422 by Rails convention), preserving all entered data.
