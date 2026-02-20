---
id: "01KHY7PZVJZ7WCN58NM39WA7D2"
name: "users_notification_setting_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/users/notification_settings_controller.rb
- app/models/users/notification_setting.rb
- app/controllers/admin/users_controller.rb
- app/controllers/api/v0/admin/users_controller.rb
- app/controllers/api/v0/users_controller.rb
- app/controllers/api/v1/admin/users_controller.rb
- app/controllers/api/v1/users_controller.rb
- app/controllers/concerns/api/admin/users_controller.rb
- app/controllers/concerns/api/users_controller.rb
- app/controllers/users/settings_controller.rb
- app/controllers/users_controller.rb
- app/helpers/admin/users_helper.rb
- spec/models/users/notification_setting_spec.rb

## Functional Overview

This specification defines the expected behavior of `Users::NotificationSetting` within the users domain.

### Behavioral Areas

- **when callbacks are triggered after commit**: enqueues SubscribeToMailchimpNewsletterWorker when updating email_newsletter to true
- **subscribing to mailchimp newsletter**: enqueues SubscribeToMailchimpNewsletterWorker when updating email_newsletter to true

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/users/notification_settings_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/users/notification_setting.rb` -- data persistence, validations, and associations
- **Controller layer**: `app/controllers/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/admin/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/users_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users/settings_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/users_controller.rb` -- HTTP request routing and response handling
- **View helper**: `app/helpers/admin/users_helper.rb` -- shared view utility methods


## Scenarios

### S-1: enqueues SubscribeToMailchimpNewsletterWorker when updating email_newsletter to ...

- **Given** the system is in a standard operational state
- **When** updating email_newsletter to true
- **Then** enqueues SubscribeToMailchimpNewsletterWorker

### S-2: enqueues SubscribeToMailchimpNewsletterWorker when updating email_newsletter to ...

- **Given** the system is in a standard operational state
- **When** updating email_newsletter to false
- **Then** enqueues SubscribeToMailchimpNewsletterWorker

### S-3: does not enqueue if email is not set

- **Given** email is not set
- **When** the action is triggered
- **Then** does not enqueue

### S-4: does not enqueue if Mailchimp is not enabled

- **Given** Mailchimp is not enabled
- **When** the action is triggered
- **Then** does not enqueue

### S-5: does not enqueue without updating email_newsletter

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not enqueue without updating email_newsletter

