---
id: "01KHY7Q0SKRYTBGZ8CTAFND2J1"
name: "notify_mailer_mailer"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/mailers/notify_mailer.rb
- app/mailers/application_mailer.rb
- app/mailers/concerns/deliverable.rb
- app/mailers/custom_mailer.rb
- app/mailers/devise_mailer.rb
- app/mailers/digest_mailer.rb
- app/mailers/organization_invitation_mailer.rb
- app/mailers/organization_membership_notification_mailer.rb
- app/mailers/survey_mailer.rb
- app/mailers/verification_mailer.rb
- spec/mailers/notify_mailer_spec.rb

## Functional Overview

This specification defines the expected behavior of `NotifyMailer` within the emails domain.

### Behavioral Areas

- **new_reply_email**: Ensures correct behavior under the specified conditions
- **new_follower_email**: Ensures correct behavior under the specified conditions
- **new_mention_email**: Ensures correct behavior under the specified conditions
- **when mentioning in a comment**: Ensures correct behavior under the specified conditions
- **when mentioning in an article**: Ensures correct behavior under the specified conditions
- **unread_notifications_email**: Ensures correct behavior under the specified conditions
- **with subforem-specific user**: includes the user URL
- **video_upload_complete_email**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Mailer**: `app/mailers/notify_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/application_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/concerns/deliverable.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/custom_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/devise_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/digest_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/organization_invitation_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/organization_membership_notification_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/survey_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/verification_mailer.rb` -- email template rendering and delivery


## Scenarios

### S-1: renders proper subject

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders proper subject

### S-2: renders proper receiver

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders proper receiver

### S-3: renders proper subject

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders proper subject

### S-4: renders proper receiver

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders proper receiver

### S-5: renders proper subject and receiver

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders proper subject and receiver

### S-6: renders proper subject and receiver

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders proper subject and receiver

### S-7: renders proper subject

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders proper subject

### S-8: renders proper receiver

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders proper receiver

### S-9: uses subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses subforem

### S-10: uses subforem

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses subforem

### S-11: renders proper subject

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders proper subject

### S-12: renders proper receiver

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders proper receiver

