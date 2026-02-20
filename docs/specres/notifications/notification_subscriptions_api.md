---
id: "01KHY7Q05TKBPS8N2243HF21ZS"
name: "notification_subscriptions_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/notification_subscriptions_controller.rb
- spec/requests/notification_subscriptions_spec.rb

## Functional Overview

This specification defines the expected behavior of `"NotificationSubscriptions"` within the notifications domain.

### Behavioral Areas

- **NotificationSubscriptions**: Ensures correct behavior under the specified conditions
- **show or GET /notification_subscriptions/:notifiable_type/:notifiable_id**: Ensures correct behavior under the specified conditions
- **when signed in**: Ensures correct behavior under the specified conditions
- **upsert or POST /notification_subscriptions/:notifiable_type/:notifiable_id**: Ensures correct behavior under the specified conditions
- **when sent as a JSON request with the correct params**: returns a JSON response
- **when an article has two parent comments by two different people**: updates the article.receive_notifications column correctly if the current_user is the author
- **when an article has a single comment thread with multiple commenters**: updates the article.receive_notifications column correctly if the current_user is the author
- **POST /comments/subscribe**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/notification_subscriptions_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns a JSON response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a JSON response

### S-2: returns the correct subscription boolean as JSON

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct subscription boolean as JSON

### S-3: returns the correct subscription boolean as JSON if unsubscribed

- **Given** unsubscribed
- **When** the action is triggered
- **Then** returns the correct subscription boolean as JSON

### S-4: returns a JSON response 

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a JSON response 

### S-5: returns 404 if there is no logged in user

- **Given** there is no logged in user
- **When** the action is triggered
- **Then** returns 404

### S-6: completes a proper subscription

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** completes a proper subscription

### S-7: removes a previous subscription

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes a previous subscription

### S-8: updates the article.receive_notifications column correctly if the current_user i...

- **Given** the current_user is the author
- **When** the action is triggered
- **Then** updates the article.receive_notifications column correctly

### S-9: updates the comment.receive_notifications column correctly if the current_user i...

- **Given** the current_user is the commenter
- **When** the action is triggered
- **Then** updates the comment.receive_notifications column correctly

### S-10: mutes the parent comment

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** mutes the parent comment

### S-11: does not mute the someone else

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not mute the someone else

### S-12: unmutes the parent comment if already muted

- **Given** already muted
- **When** the action is triggered
- **Then** unmutes the parent comment

