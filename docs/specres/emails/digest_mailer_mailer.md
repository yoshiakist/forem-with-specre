---
id: "01KHY7Q0SHQ9BXNJP9XGMW2MMN"
name: "digest_mailer_mailer"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/mailers/digest_mailer.rb
- app/mailers/application_mailer.rb
- app/mailers/concerns/deliverable.rb
- app/mailers/custom_mailer.rb
- app/mailers/devise_mailer.rb
- app/mailers/notify_mailer.rb
- app/mailers/organization_invitation_mailer.rb
- app/mailers/organization_membership_notification_mailer.rb
- app/mailers/survey_mailer.rb
- app/mailers/verification_mailer.rb
- spec/mailers/digest_mailer_spec.rb

## Functional Overview

This specification defines the expected behavior of `DigestMailer` within the emails domain.

### Behavioral Areas

- **digest_email**: Ensures correct behavior under the specified conditions
- **generate_title**: Ensures correct behavior under the specified conditions
- **when user follows no subforems**: uses Forem Digest in subject when onboarding subforem is not default
- **when user follows one subforem**: uses Forem Digest in subject when onboarding subforem is not default
- **when user follows multiple subforems**: uses Forem Digest in subject when onboarding subforem is not default
- **when not on DEV.to**: uses Forem Digest in subject when onboarding subforem is not default
- **when user has custom onboarding subforem**: uses Forem Digest in subject when onboarding subforem is not default

### Implementation Architecture

The behavior is implemented across the following layers:

- **Mailer**: `app/mailers/digest_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/application_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/concerns/deliverable.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/custom_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/devise_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/notify_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/organization_invitation_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/organization_membership_notification_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/survey_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/verification_mailer.rb` -- email template rendering and delivery


## Scenarios

### S-1: works correctly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** works correctly

### S-2: includes the correct X-SMTPAPI header for SendGrid

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes the correct X-SMTPAPI header for SendGrid

### S-3: includes billboard html in body

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes billboard html in body

### S-4: uses DEV Digest in subject

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses DEV Digest in subject

### S-5: uses Forem Digest in subject

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses Forem Digest in subject

### S-6: uses Forem Digest in subject

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses Forem Digest in subject

### S-7: does not include digest suffix

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not include digest suffix

### S-8: uses Forem Digest in subject when onboarding subforem is not default

- **Given** the system is in a standard operational state
- **When** onboarding subforem is not default
- **Then** uses Forem Digest in subject

### S-9: uses DEV Digest in subject when onboarding subforem is default

- **Given** the system is in a standard operational state
- **When** onboarding subforem is default
- **Then** uses DEV Digest in subject

