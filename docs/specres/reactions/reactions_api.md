---
id: "01KHY7Q0G9THKVWC551K993X50"
name: "reactions_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/privileged_reactions_controller.rb
- app/controllers/admin/reactions_controller.rb
- app/controllers/api/v1/reactions_controller.rb
- app/controllers/reactions_controller.rb
- app/services/users/confirm_flag_reactions.rb
- app/workers/users/confirm_flag_reactions_worker.rb
- spec/requests/reactions_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Reactions"` within the reactions domain.

### Behavioral Areas

- **Reactions**: sets the surrogate key header for article reactions
- **GET /reactions?article_id=:article_id**: Ensures correct behavior under the specified conditions
- **when signed in**: returns a 429 status when rate limit is reached
- **when signed out**: returns a 429 status when rate limit is reached
- **GET /reactions?commentable_id=:article.id&commentable_type=Article**: Ensures correct behavior under the specified conditions
- **when signed in**: returns a 429 status when rate limit is reached
- **when signed out**: returns a 429 status when rate limit is reached
- **POST /reactions**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/privileged_reactions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/reactions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/reactions_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/reactions_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/users/confirm_flag_reactions.rb` -- business logic orchestration and domain operations
- **Background worker**: `app/workers/users/confirm_flag_reactions_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: returns the correct json response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct json response

### S-2: does not set Surrogate-Key cache control headers

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not set Surrogate-Key cache control headers

### S-3: does not set X-Accel-Expires headers

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not set X-Accel-Expires headers

### S-4: does not set Fastly cache control and surrogate control headers

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not set Fastly cache control and surrogate control headers

### S-5: returns the correct json response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct json response

### S-6: sets the surrogate key header for article reactions

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the surrogate key header for article reactions

### S-7: sets the x-accel-expires header equal to max-age for article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the x-accel-expires header equal to max-age for article

### S-8: sets Fastly cache control and surrogate control headers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets Fastly cache control and surrogate control headers

### S-9: returns the correct json response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct json response

### S-10: does not set surrogate key headers

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not set surrogate key headers

### S-11: does not set x-accel-expires headers

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not set x-accel-expires headers

### S-12: does not set Fastly cache control and surrogate control headers

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not set Fastly cache control and surrogate control headers

