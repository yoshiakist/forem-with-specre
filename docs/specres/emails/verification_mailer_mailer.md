---
id: "01KHY7Q0SSTR6QNE6N31JZ9H4C"
name: "verification_mailer_mailer"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/mailers/verification_mailer.rb
- app/mailers/application_mailer.rb
- app/mailers/concerns/deliverable.rb
- app/mailers/custom_mailer.rb
- app/mailers/devise_mailer.rb
- app/mailers/digest_mailer.rb
- app/mailers/notify_mailer.rb
- app/mailers/organization_invitation_mailer.rb
- app/mailers/organization_membership_notification_mailer.rb
- app/mailers/survey_mailer.rb
- spec/mailers/verification_mailer_spec.rb

## Functional Overview

This specification defines the expected behavior of `VerificationMailer` within the emails domain.

### Behavioral Areas

- **account_ownership_verification_email**: Ensures correct behavior under the specified conditions
- **with subforem-specific branding**: Ensures correct behavior under the specified conditions
- **magic_link**: Ensures correct behavior under the specified conditions
- **with subforem-specific branding**: Ensures correct behavior under the specified conditions
- **with nil onboarding_subforem_id**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Mailer**: `app/mailers/verification_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/application_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/concerns/deliverable.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/custom_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/devise_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/digest_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/notify_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/organization_invitation_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/organization_membership_notification_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/survey_mailer.rb` -- email template rendering and delivery


## Scenarios

### S-1: works correctly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** works correctly

### S-2: uses subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses subforem

### S-3: uses subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses subforem

### S-4: sends a magic link email

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends a magic link email

### S-5: does not include the generic magic link copy

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not include the generic magic link copy

### S-6: uses subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses subforem

### S-7: uses subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses subforem

### S-8: includes subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes subforem

### S-9: uses subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses subforem

### S-10: falls back to default subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** falls back to default subforem

### S-11: falls back to default subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** falls back to default subforem

