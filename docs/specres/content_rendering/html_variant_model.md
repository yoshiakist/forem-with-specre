---
id: "01KHY7Q1CFM0K75Q31EBNF43RE"
name: "html_variant_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/html_variants_controller.rb
- app/models/html_variant.rb
- app/policies/html_variant_policy.rb
- spec/models/html_variant_spec.rb

## Functional Overview

This specification defines the expected behavior of `HtmlVariant` within the content_rendering domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/html_variants_controller.rb` -- HTTP request routing and response handling
- **Model layer**: `app/models/html_variant.rb` -- data persistence, validations, and associations
- **Policy layer**: `app/policies/html_variant_policy.rb` -- authorization and access control rules


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to user.optional
- validate inclusion of group.in array described class::GROUP NAMES
- validate presence of html
- validate uniqueness of name

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: prefixes an image with cloudinary

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** prefixes an image with cloudinary

### S-3: does not add prefix if it already starts with cloudinary

- **Given** it already starts with cloudinary
- **When** the action is triggered
- **Then** does not add prefix

### S-4: does not add prefix if already on site root

- **Given** already on site root
- **When** the action is triggered
- **Then** does not add prefix

### S-5: strips whitespace from the name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** strips whitespace from the name

