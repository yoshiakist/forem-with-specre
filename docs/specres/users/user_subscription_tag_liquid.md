---
id: "01KHY7PZSZ2M51FX5NFF0PWJHY"
name: "user_subscription_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/user_subscription_tag.rb
- app/models/liquid_tags/user_subscription_tag.rb
- app/liquid_tags/user_tag.rb
- app/services/users/approved_liquid_tags.rb
- spec/liquid_tags/user_subscription_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `UserSubscriptionTag` within the users domain.

### Behavioral Areas

- **.user_authorization_method_name**: Ensures correct behavior under the specified conditions
- **when rendering**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/user_subscription_tag.rb` -- custom Markdown/Liquid embed rendering
- **Model layer**: `app/models/liquid_tags/user_subscription_tag.rb` -- data persistence, validations, and associations
- **Liquid tag**: `app/liquid_tags/user_tag.rb` -- custom Markdown/Liquid embed rendering
- **Service layer**: `app/services/users/approved_liquid_tags.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- eq user subscription tag available?

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: renders default data correctly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders default data correctly

