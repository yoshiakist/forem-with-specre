---
id: "01KHY7Q1CJ68P2S04GQJKNNGX3"
name: "html_variant_policy_policy"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/policies/html_variant_policy.rb
- spec/policies/html_variant_policy_spec.rb

## Functional Overview

This specification defines the expected behavior of `HtmlVariantPolicy` within the content_rendering domain.

### Behavioral Areas

- **when user is not an admin**: Ensures correct behavior under the specified conditions
- **when user is an admin**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Policy layer**: `app/policies/html_variant_policy.rb` -- authorization and access control rules


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- forbid actions %i[index show edit update create]
- permit actions %i[index show edit update create]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

