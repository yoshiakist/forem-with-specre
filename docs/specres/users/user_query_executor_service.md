---
id: "01KHY7PZZ4J50A05HYTVJKA1XW"
name: "user_query_executor_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/user_query_executor.rb
- app/services/articles/feeds/article_score_calculator_for_user.rb
- app/services/articles/get_user_stickies.rb
- app/services/authentication/authenticator.rb
- app/services/authentication/paths.rb
- app/services/authentication/providers.rb
- app/services/authentication/providers/apple.rb
- app/services/authentication/providers/facebook.rb
- app/services/authentication/providers/forem.rb
- app/services/authentication/providers/github.rb
- app/services/authentication/providers/google_oauth2.rb
- spec/services/user_query_executor_spec.rb

## Functional Overview

This specification defines the expected behavior of `UserQueryExecutor` within the users domain.

### Behavioral Areas

- **initialize**: Ensures correct behavior under the specified conditions
- **valid?**: Ensures correct behavior under the specified conditions
- **execute**: executes the query and returns users
- **test_execute**: Ensures correct behavior under the specified conditions
- **estimated_count**: Ensures correct behavior under the specified conditions
- **error handling**: handles query execution errors gracefully
- **execution environment setup**: handles query execution errors gracefully
- **query building**: returns false for inactive user query

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/user_query_executor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/article_score_calculator_for_user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/get_user_stickies.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/authenticator.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/paths.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/apple.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/facebook.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/forem.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/github.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/authentication/providers/google_oauth2.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: sets up the executor with valid parameters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets up the executor with valid parameters

### S-2: accepts custom timeout and limit

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts custom timeout and limit

### S-3: returns true for valid executor

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns true for valid executor

### S-4: returns false for inactive user query

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false for inactive user query

### S-5: returns false for invalid timeout

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false for invalid timeout

### S-6: returns false for invalid limit

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false for invalid limit

### S-7: executes the query and returns users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** executes the query and returns users

### S-8: respects the limit parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** respects the limit parameter

### S-9: returns empty result for invalid query

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns empty result for invalid query

### S-10: returns empty result for inactive query

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns empty result for inactive query

### S-11: handles query validation failures

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles query validation failures

### S-12: executes with limited number of users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** executes with limited number of users

