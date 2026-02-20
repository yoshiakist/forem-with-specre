---
id: "01KHY7PZTY8VRF8VJG0E0CETA2"
name: "user_query_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/user_query.rb
- app/services/user_query_executor.rb
- app/services/user_query_validator.rb
- app/services/user_query_variable_substitutor.rb
- app/models/banished_user.rb
- app/models/concerns/algolia_searchable/searchable_user.rb
- app/models/concerns/user_subscription_sourceable.rb
- app/models/gdpr_delete_request.rb
- app/models/identity.rb
- app/models/liquid_tags/user_subscription_tag.rb
- app/models/segmented_user.rb
- app/models/settings/authentication.rb
- app/models/settings/user_experience.rb
- app/models/user.rb
- spec/models/user_query_spec.rb

## Functional Overview

This specification defines the expected behavior of `UserQuery` within the users domain.

### Behavioral Areas

- **associations**: Ensures correct behavior under the specified conditions
- **validations**: Ensures correct behavior under the specified conditions
- **query validation**: executes the query and returns users
- **scopes**: Ensures correct behavior under the specified conditions
- **.active**: Ensures correct behavior under the specified conditions
- **.recently_executed**: Ensures correct behavior under the specified conditions
- **execute_safely**: Ensures correct behavior under the specified conditions
- **test_execution**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/user_query.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/user_query_executor.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/user_query_validator.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/user_query_variable_substitutor.rb` -- business logic orchestration and domain operations
- **Model layer**: `app/models/banished_user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/user_subscription_sourceable.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/gdpr_delete_request.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/identity.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/liquid_tags/user_subscription_tag.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/segmented_user.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/settings/authentication.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to created by.class name "User"
- have many emails.dependent nullify
- validate presence of name
- validate presence of query
- belong to created by
- validate presence of max execution time ms
- validate uniqueness of name
- validate length of name.is at most 255
- validate length of description.is at most 1000
- validate length of query.is at most 10 000

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: rejects queries that don

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects queries that don

### S-3: rejects queries that don

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects queries that don

### S-4: rejects queries that don

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects queries that don

### S-5: rejects queries with forbidden keywords

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects queries with forbidden keywords

### S-6: rejects queries with suspicious patterns

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects queries with suspicious patterns

### S-7: accepts queries with unbalanced parentheses (not validated by model)

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts queries with unbalanced parentheses (not validated by model)

### S-8: accepts valid queries

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts valid queries

### S-9: accepts queries with joins

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts queries with joins

### S-10: returns only active queries

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only active queries

### S-11: returns only queries that have been executed

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only queries that have been executed

### S-12: orders by last_executed_at descending

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** orders by last_executed_at descending

### S-13: executes the query and returns users

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** executes the query and returns users

