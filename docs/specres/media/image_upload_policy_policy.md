---
id: "01KHY7Q160NRJTPVBWJEMS1N3Z"
name: "image_upload_policy_policy"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/policies/image_upload_policy.rb
- spec/policies/image_upload_policy_spec.rb

## Functional Overview

This specification defines the expected behavior of `ImageUploadPolicy` within the media domain.

### Behavioral Areas

- **when user is not signed in**: Ensures correct behavior under the specified conditions
- **when user is signed in**: Ensures correct behavior under the specified conditions
- **when user is suspended**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Policy layer**: `app/policies/image_upload_policy.rb` -- authorization and access control rules


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- permit actions %i[create]
- forbid actions %i[create]

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

