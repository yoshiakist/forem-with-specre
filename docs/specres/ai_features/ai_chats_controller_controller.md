---
id: "01KHY7Q0Y0XVHZN4B2BD6S2JXX"
name: "ai_chats_controller_controller"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/ai_chats_controller.rb
- app/controllers/ai_image_generations_controller.rb
- spec/controllers/ai_chats_controller_spec.rb

## Functional Overview

This specification defines the expected behavior of `AiChatsController` within the ai_features domain.

### Behavioral Areas

- **GET #index**: Ensures correct behavior under the specified conditions
- **when user is an admin**: Ensures correct behavior under the specified conditions
- **when user is not an admin**: Ensures correct behavior under the specified conditions
- **when user is not logged in**: Ensures correct behavior under the specified conditions
- **POST #create**: Ensures correct behavior under the specified conditions
- **when user is an admin**: Ensures correct behavior under the specified conditions
- **when user is not an admin**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/ai_chats_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/ai_image_generations_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns a success response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a success response

### S-2: redirects to root path

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to root path

### S-3: redirects to sign in

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to sign in

### S-4: returns success with AI message

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns success with AI message

### S-5: returns error if message is blank

- **Given** message is blank
- **When** the action is triggered
- **Then** returns error

### S-6: returns unauthorized for JSON requests

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns unauthorized for JSON requests

