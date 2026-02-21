---
id: "01KHZME2KMA2REG6V4QSGBK5XQ"
name: "admin_can_edit_survey"
status: "draft"
---

## Related Files

- `app/controllers/admin/surveys_controller.rb`
- `app/javascript/admin/controllers/admin_surveys_controller.js`
- `spec/requests/admin/surveys_spec.rb` (Test)
- `app/views/admin/surveys/edit.html.erb` (Template)
- `app/views/admin/surveys/_form.html.erb` (Template)
- `app/views/admin/surveys/_poll_fields.html.erb` (Template)

## Functional Overview

An admin loads the edit form for an existing survey, modifies its title, settings, or nested polls, and submits the update. The `edit` action fetches the survey by ID and renders the shared form partial. On submission, the `update` action applies permitted parameters via Rails nested attributes, which allows adding new polls, modifying existing ones (prompt, type, options, position), and marking polls or options for destruction — all in a single request. The Stimulus controller (`admin-surveys`) manages the dynamic form UI: it adds or removes poll blocks without a page reload, toggles section visibility (options vs. scale fields) based on the selected poll type, and adds or removes individual poll options inline. A successful update redirects to the surveys index with a success flash message; validation failure re-renders the edit form with an inline error message.

## Design Intent

The form uses Rails nested attributes (`accepts_nested_attributes_for`) with `_destroy` flags to handle poll and option removal server-side, avoiding the need for separate AJAX delete requests. The Stimulus controller uses a `<template>` tag containing a poll partial rendered with a `NEW_RECORD` placeholder index; when "Add Poll" is clicked, the template HTML is cloned with a timestamp-based index to ensure uniqueness before a save. This allows zero-backend-round-trip poll addition while remaining compatible with standard Rails form submission.

## Key Members

- `survey_params` — strong parameters permitting `:title`, `:active`, `:display_title`, `:allow_resubmission`, `:daily_email_distributions`, `:extra_email_context_paragraph`, and `polls_attributes` (including nested `poll_options_attributes`) with `:id` and `:_destroy` fields for nested destruction
- Stimulus targets: `pollContainer` (DOM node where poll blocks are appended), `pollTemplate` (hidden `<template>` element), `poll` (each poll block), `optionsContainer` (per-poll options list)

## Scenarios

### Update survey title and settings

1. Admin navigates to the edit page for an existing survey; the form pre-populates all current field values.
2. Admin changes the title, toggles checkboxes (active, display title, allow resubmission), adjusts daily email distribution count or email context text.
3. Admin submits the form.
4. The server finds the survey by ID, applies the permitted parameters, and saves the record.
5. Admin is redirected to the surveys index page with a success flash message.

### Add a new poll to an existing survey

1. On the edit form, admin clicks "Add Poll".
2. The Stimulus controller clones the hidden poll template, substitutes the `NEW_RECORD` placeholder with a timestamp-based index, and appends the new poll block to the poll container.
3. Admin fills in the question prompt, selects a poll type, and (for single/multiple choice types) adds one or more options.
4. Admin submits the form.
5. The server processes the nested poll attributes and persists the new poll (and its options) alongside the existing polls.

### Change poll type and observe UI section toggle

1. On the edit form, admin changes the type dropdown of an existing poll.
2. The Stimulus controller's `handleTypeChange` method is triggered and calls `updateVisibility` for that poll block.
3. If the type is `text_input`, both the options section and scale section are hidden.
4. If the type is `scale`, the scale section (min/max fields) is shown and the options section is hidden.
5. If the type is `single_choice` or `multiple_choice`, the options section is shown and the scale section is hidden.

### Remove a poll from an existing survey

1. Admin clicks "Remove Poll" on a poll block that already exists in the database (has an `id`).
2. The Stimulus controller sets the hidden `_destroy` field to `1` and hides the poll block visually.
3. Admin submits the form.
4. The server processes the `_destroy: "1"` flag in the nested attributes and deletes the poll record.

### Validation failure on update

1. Admin submits the edit form with invalid data (e.g., blank title).
2. The server attempts to update the survey; the model validation fails.
3. The `update` action re-renders the edit template with a danger flash message containing the validation errors.
4. Admin remains on the edit page and can correct the errors.

## Failures / Exceptions

- If the survey is not found by the given ID, Rails raises `ActiveRecord::RecordNotFound` (handled by the application's default error handling).
- On validation failure, `@survey.errors_as_sentence` is placed in `flash.now[:danger]` and the edit template is re-rendered (HTTP 200 with the form, not a redirect).
