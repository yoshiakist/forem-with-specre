---
id: "01KHY7Q0S8GJ2WZQBHZRPKTQYZ"
name: "application_mailer_mailer"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/mailers/application_mailer.rb
- app/mailers/concerns/deliverable.rb
- app/mailers/custom_mailer.rb
- app/mailers/devise_mailer.rb
- app/mailers/digest_mailer.rb
- app/mailers/notify_mailer.rb
- app/mailers/organization_invitation_mailer.rb
- app/mailers/organization_membership_notification_mailer.rb
- app/mailers/survey_mailer.rb
- app/mailers/verification_mailer.rb
- spec/mailers/application_mailer_spec.rb

## Functional Overview

This specification defines the expected behavior of `ApplicationMailer` within the emails domain.

### Behavioral Areas

- **set_perform_deliveries**: Ensures correct behavior under the specified conditions
- **set_delivery_options**: Ensures correct behavior under the specified conditions
- **magic link heads up logic**: includes the magic link heads up if user has no page views past 4 weeks
- **setup_subforem_context**: Ensures correct behavior under the specified conditions
- **when user has onboarding_subforem_id**: includes the magic link heads up if user has no page views past 4 weeks
- **when user has nil onboarding_subforem_id**: includes the magic link heads up if user has no page views past 4 weeks
- **when subforem_id doesn**: sets subforem_id from user
- **when no subforems exist**: includes topic in from address when provided

### Implementation Architecture

The behavior is implemented across the following layers:

- **Mailer**: `app/mailers/application_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/concerns/deliverable.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/custom_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/devise_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/digest_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/notify_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/organization_invitation_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/organization_membership_notification_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/survey_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/verification_mailer.rb` -- email template rendering and delivery


## Scenarios

### S-1: changes perform_deliveries from true to false if smtp is not enabled

- **Given** smtp is not enabled
- **When** the action is triggered
- **Then** changes perform_deliveries from true to false

### S-2: changes perform_deliveries from false to true if smtp is enabled

- **Given** smtp is enabled
- **When** the action is triggered
- **Then** changes perform_deliveries from false to true

### S-3: sets proper SMTP credential during callback

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets proper SMTP credential during callback

### S-4: includes the magic link heads up if user has no page views past 4 weeks

- **Given** user has no page views past 4 weeks
- **When** the action is triggered
- **Then** includes the magic link heads up

### S-5: does not include the magic link heads up if user has page views past 4 weeks

- **Given** user has page views past 4 weeks
- **When** the action is triggered
- **Then** does not include the magic link heads up

### S-6: sets subforem_id from user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets subforem_id from user

### S-7: sets subforem_domain from the subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets subforem_domain from the subforem

### S-8: uses the subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses the subforem

### S-9: falls back to default subforem_id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** falls back to default subforem_id

### S-10: uses default subforem domain

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses default subforem domain

### S-11: falls back to default domain

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** falls back to default domain

### S-12: falls back to Settings::General.app_domain

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** falls back to Settings::General.app_domain

