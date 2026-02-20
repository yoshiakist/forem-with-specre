---
id: "01KHY7Q11DNYTVBYM6FXP5G1GR"
name: "admin_feedback_messages_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/feedback_messages_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/moderation/reports"` within the admin domain.

### Behavioral Areas

- **/admin/moderation/reports**: Ensures correct behavior under the specified conditions
- **GET /admin/moderation/reports**: Ensures correct behavior under the specified conditions
- **when the user is a single resource admin**: Ensures correct behavior under the specified conditions
- **when there is a vomit reaction on a user with score > -150 and created in the last two weeks**: renders with status 200
- **POST /admin/moderation/reports/save_status**: Ensures correct behavior under the specified conditions
- **when a valid request is made**: Ensures correct behavior under the specified conditions
- **POST /send_email**: Ensures correct behavior under the specified conditions
- **when a valid request is made**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: renders with status 200

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders with status 200

### S-2: renders with status 200

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders with status 200

### S-3: does not render if the reaction is older than two weeks

- **Given** the reaction is older than two weeks
- **When** the action is triggered
- **Then** does not render

### S-4: does not render if the reactable score is <= -150

- **Given** the reactable score is <= -150
- **When** the action is triggered
- **Then** does not render

### S-5: returns a JSON with an outcome key and Success value

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a JSON with an outcome key and Success value

### S-6: updates the status of the feedback message

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the status of the feedback message

### S-7: returns a JSON with an outcome key and Success value

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a JSON with an outcome key and Success value

### S-8: creates a new email message with the same params

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new email message with the same params

### S-9: renders the proper JSON response

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper JSON response

### S-10: creates a note with the correct params

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a note with the correct params

### S-11: queues a slack message to be sent

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** queues a slack message to be sent

