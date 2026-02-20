---
id: "01KHY7Q05MP77C9PNF7RFYFF8T"
name: "notification_subscription_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/notification_subscriptions_controller.rb
- app/models/notification_subscription.rb
- app/models/context_notification.rb
- app/models/notification.rb
- app/models/users/notification_setting.rb
- app/models/welcome_notification.rb
- spec/models/notification_subscription_spec.rb

## Functional Overview

This specification defines the expected behavior of `NotificationSubscription` within the notifications domain.

### Behavioral Areas

- **notifiable_type**: Ensures correct behavior under the specified conditions
- **.for_notifiable**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/notification_subscriptions_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/notification_subscription.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/context_notification.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/notification.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/users/notification_setting.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/welcome_notification.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to notifiable
- belong to user
- validate presence of config
- validate presence of notifiable type
- validate uniqueness of user id.scoped to %i[notifiable type notifiable id]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: validates config

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** validates config

### S-3: is valid if equals to Article

- **Given** equals to Article
- **When** the action is triggered
- **Then** is valid

### S-4: is valid if equals to Comment

- **Given** equals to Comment
- **When** the action is triggered
- **Then** is valid

### S-5: is is invalid with Podcast

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is is invalid with Podcast

### S-6: can find subscription if given a notifiable object

- **Given** given a notifiable object
- **When** the action is triggered
- **Then** can find subscription

### S-7: can find subscription if given id & type

- **Given** given id & type
- **When** the action is triggered
- **Then** can find subscription

### S-8: update_notification_subscriptions calls UpdateWorker later

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** update_notification_subscriptions calls UpdateWorker later

