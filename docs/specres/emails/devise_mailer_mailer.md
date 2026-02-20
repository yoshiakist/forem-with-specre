---
id: "01KHY7Q0SE292ET10V879GYXE4"
name: "devise_mailer_mailer"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/mailers/devise_mailer.rb
- app/mailers/application_mailer.rb
- app/mailers/concerns/deliverable.rb
- app/mailers/custom_mailer.rb
- app/mailers/digest_mailer.rb
- app/mailers/notify_mailer.rb
- app/mailers/organization_invitation_mailer.rb
- app/mailers/organization_membership_notification_mailer.rb
- app/mailers/survey_mailer.rb
- app/mailers/verification_mailer.rb
- spec/mailers/devise_mailer_spec.rb

## Functional Overview

This specification defines the expected behavior of `DeviseMailer` within the emails domain.

### Behavioral Areas

- **reset_password_instructions**: Ensures correct behavior under the specified conditions
- **confirmation_instructions**: Ensures correct behavior under the specified conditions
- **when it**: Ensures correct behavior under the specified conditions
- **when it**: Ensures correct behavior under the specified conditions
- **when user has an onboarding_subforem_id**: sends emails to each user with their respective subforem
- **when user has no onboarding_subforem_id**: sends emails to each user with their respective subforem
- **invitation_instructions**: Ensures correct behavior under the specified conditions
- **edge cases**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Mailer**: `app/mailers/devise_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/application_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/concerns/deliverable.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/custom_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/digest_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/notify_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/organization_invitation_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/organization_membership_notification_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/survey_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/verification_mailer.rb` -- email template rendering and delivery


## Scenarios

### S-1: renders sender

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders sender

### S-2: renders a reply to email address

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders a reply to email address

### S-3: renders proper URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders proper URL

### S-4: does not include Ahoy click tracking parameters

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not include Ahoy click tracking parameters

### S-5: renders the correct body

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the correct body

### S-6: renders proper URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders proper URL

### S-7: renders the correct body

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the correct body

### S-8: renders proper URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders proper URL

### S-9: includes name in welcome email

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes name in welcome email

### S-10: does not include name in confirmation email if includes http

- **Given** includes http
- **When** the action is triggered
- **Then** does not include name in confirmation email

### S-11: uses the subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses the subforem

### S-12: uses the subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses the subforem

