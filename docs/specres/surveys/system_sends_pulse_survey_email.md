---
id: "01KJ2HPE39M61JKHQGRA7AHD0D"
name: "system_sends_pulse_survey_email"
status: "draft"
---

## Related Files

- `app/mailers/survey_mailer.rb`
- `app/views/mailers/survey_mailer/pulse_survey.html.erb` (Template)
- `spec/mailers/survey_mailer_spec.rb` (Test)

## Functional Overview

`SurveyMailer#pulse_survey` sends an invitation email to a user asking them to participate in a community pulse survey. The mailer receives a `user` and a `survey` via `params`, resolves the community name from `Settings::Community` (scoped to the current subforem), and sends an email with a subject line that includes the community name. The email body addresses the user by name, explains they have been randomly selected, optionally includes an extra context paragraph from the survey configuration, and provides a prominent call-to-action link to the survey page (via `survey_url(@survey.slug)`). The email assures the user that responses are anonymous.

## Key Members

- `params[:user]` — the `User` record receiving the email
- `params[:survey]` — the `Survey` record being promoted
- `@community_name` — resolved via `Settings::Community.community_name(subforem_id:)` for branding
- `survey.extra_email_context_paragraph` — optional free-text paragraph that the admin can set when creating the survey, rendered between the introduction and the CTA link

## Scenarios

### Sending a pulse survey email with extra context

1. `SurveyMailer.with(user: user, survey: survey).pulse_survey.deliver_later` is called.
2. The mailer resolves the community name for the current subforem.
3. The email is sent to `user.email` with subject "You've been randomly selected for a {community} Pulse Survey".
4. The email body includes the user's name, the explanation text, the survey's `extra_email_context_paragraph`, and a link to `survey_url(survey.slug)`.

### Sending a pulse survey email without extra context

1. Same as above, but `survey.extra_email_context_paragraph` is blank.
2. The conditional block in the template is skipped; the email body goes directly from the introduction to the CTA link.

## Failures / Exceptions

- If `user.email` is nil or invalid, the email delivery will fail at the mail transport layer; this is handled by the standard ActionMailer/ActiveJob retry mechanism.
