---
id: "01KHY7Q0SPE22H49Y79AZYKZNY"
name: "survey_mailer_mailer"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/mailers/survey_mailer.rb
- app/mailers/application_mailer.rb
- app/mailers/concerns/deliverable.rb
- app/mailers/custom_mailer.rb
- app/mailers/devise_mailer.rb
- app/mailers/digest_mailer.rb
- app/mailers/notify_mailer.rb
- app/mailers/organization_invitation_mailer.rb
- app/mailers/organization_membership_notification_mailer.rb
- app/mailers/verification_mailer.rb
- spec/mailers/survey_mailer_spec.rb

## Functional Overview

This specification defines the expected behavior of `SurveyMailer` within the emails domain.

### Behavioral Areas

- **pulse_survey**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Mailer**: `app/mailers/survey_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/application_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/concerns/deliverable.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/custom_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/devise_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/digest_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/notify_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/organization_invitation_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/organization_membership_notification_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/verification_mailer.rb` -- email template rendering and delivery


## Scenarios

### S-1: renders the headers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the headers

### S-2: renders the body with link to survey

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the body with link to survey

