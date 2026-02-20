---
id: "01KHY7Q0SBS9BARJ1VPGFC4ZY5"
name: "custom_mailer_mailer"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/mailers/custom_mailer.rb
- app/mailers/application_mailer.rb
- app/mailers/concerns/deliverable.rb
- app/mailers/devise_mailer.rb
- app/mailers/digest_mailer.rb
- app/mailers/notify_mailer.rb
- app/mailers/organization_invitation_mailer.rb
- app/mailers/organization_membership_notification_mailer.rb
- app/mailers/survey_mailer.rb
- app/mailers/verification_mailer.rb
- spec/mailers/custom_mailer_spec.rb

## Functional Overview

This specification defines the expected behavior of `CustomMailer` within the emails domain.

### Behavioral Areas

- **custom_email**: Ensures correct behavior under the specified conditions
- **when SendGrid is enabled**: includes the from topic in the from address based on the email type when onboarding
- **when there is an email passed**: tracks the email_id after delivery
- **when from_name param is passed**: includes the from topic in the from address based on the email type when onboarding
- **when SendGrid is disabled**: includes the from topic in the from address based on the email type when onboarding

### Implementation Architecture

The behavior is implemented across the following layers:

- **Mailer**: `app/mailers/custom_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/application_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/concerns/deliverable.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/devise_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/digest_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/notify_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/organization_invitation_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/organization_membership_notification_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/survey_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/verification_mailer.rb` -- email template rendering and delivery


## Scenarios

### S-1: sets the X-SMTPAPI header with the correct category

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the X-SMTPAPI header with the correct category

### S-2: replaces the *|name|* merge tag in content and subject

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** replaces the *|name|* merge tag in content and subject

### S-3: tracks the email_id after delivery

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** tracks the email_id after delivery

### S-4: includes the from topic in the from address based on the email type when onboard...

- **Given** the system is in a standard operational state
- **When** onboarding
- **Then** includes the from topic in the from address based on the email type

### S-5: includes the from topic in the from address based on the email type when newslet...

- **Given** the system is in a standard operational state
- **When** newsletter
- **Then** includes the from topic in the from address based on the email type

### S-6: includes the from topic in the from address based on the email type when one_off

- **Given** the system is in a standard operational state
- **When** one_off
- **Then** includes the from topic in the from address based on the email type

### S-7: uses the from_name param instead of querying the Email record

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses the from_name param instead of querying the Email record

### S-8: falls back to Email lookup when from_name is nil

- **Given** the system is in a standard operational state
- **When** from_name is nil
- **Then** falls back to Email lookup

### S-9: falls back to Email lookup when from_name is not provided

- **Given** the system is in a standard operational state
- **When** from_name is not provided
- **Then** falls back to Email lookup

### S-10: does not set the X-SMTPAPI header

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not set the X-SMTPAPI header

### S-11: replaces the *|name|* merge tag in content and subject

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** replaces the *|name|* merge tag in content and subject

