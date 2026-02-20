---
id: "01KHY7Q0HEKJK20279HH9BNAF5"
name: "organization_membership_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/organization_memberships_controller.rb
- app/mailers/organization_membership_notification_mailer.rb
- app/models/organization_membership.rb
- app/models/concerns/algolia_searchable/searchable_organization.rb
- app/models/organization.rb
- spec/models/organization_membership_spec.rb

## Functional Overview

This specification defines the expected behavior of `OrganizationMembership` within the organizations domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **scopes**: Ensures correct behavior under the specified conditions
- **.pending**: Ensures correct behavior under the specified conditions
- **.active**: Ensures correct behavior under the specified conditions
- **pending?**: Ensures correct behavior under the specified conditions
- **confirm!**: Ensures correct behavior under the specified conditions
- **invitation_token generation**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/organization_memberships_controller.rb` -- HTTP request routing and response handling
- **Mailer**: `app/mailers/organization_membership_notification_mailer.rb` -- email template rendering and delivery
- **Model layer**: `app/models/organization_membership.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_organization.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/organization.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- validate presence of type of user
- validate uniqueness of user id.scoped to organization id
- validate inclusion of type of user.in array OrganizationMembership::USER TYPES

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: returns only pending memberships

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only pending memberships

### S-3: returns only non-pending memberships

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only non-pending memberships

### S-4: returns true for pending memberships

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns true for pending memberships

### S-5: returns false for non-pending memberships

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns false for non-pending memberships

### S-6: changes type_of_user from pending to member

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** changes type_of_user from pending to member

### S-7: updates the membership

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the membership

### S-8: generates an invitation token for pending memberships

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates an invitation token for pending memberships

### S-9: does not generate an invitation token for non-pending memberships

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not generate an invitation token for non-pending memberships

### S-10: preserves existing invitation token if present

- **Given** present
- **When** the action is triggered
- **Then** preserves existing invitation token

