---
id: "01KHY7Q0HHS67P4YAY31EF9E9G"
name: "organization_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/organization_memberships_controller.rb
- app/controllers/admin/organizations_controller.rb
- app/controllers/api/v0/organizations_controller.rb
- app/controllers/api/v1/organizations_controller.rb
- app/controllers/concerns/api/organizations_controller.rb
- app/controllers/organizations_controller.rb
- app/decorators/organization_decorator.rb
- app/helpers/admin/organizations_helper.rb
- app/helpers/organization_helper.rb
- app/liquid_tags/organization_tag.rb
- app/mailers/organization_invitation_mailer.rb
- app/mailers/organization_membership_notification_mailer.rb
- app/models/concerns/algolia_searchable/searchable_organization.rb
- app/models/organization.rb
- app/models/organization_membership.rb
- spec/models/organization_spec.rb

## Functional Overview

This specification defines the expected behavior of `Organization` within the organizations domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions
- **builtin validations**: Ensures correct behavior under the specified conditions
- **when callbacks are triggered before save**: triggers cache busting on save
- **name**: rejects names with over 50 characters
- **summary**: Ensures correct behavior under the specified conditions
- **text_color_hex**: Ensures correct behavior under the specified conditions
- **slug**: accepts properly formatted slug
- **when callbacks are triggered after save**: triggers cache busting on save

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/admin/organization_memberships_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/admin/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v0/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/concerns/api/organizations_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/organizations_controller.rb` -- HTTP request routing and response handling
- **Decorator**: `app/decorators/organization_decorator.rb` -- presentation logic and view-model enrichment
- **View helper**: `app/helpers/admin/organizations_helper.rb` -- shared view utility methods
- **View helper**: `app/helpers/organization_helper.rb` -- shared view utility methods
- **Liquid tag**: `app/liquid_tags/organization_tag.rb` -- custom Markdown/Liquid embed rendering
- **Mailer**: `app/mailers/organization_invitation_mailer.rb` -- email template rendering and delivery
- **Mailer**: `app/mailers/organization_membership_notification_mailer.rb` -- email template rendering and delivery


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- have many articles.dependent nullify
- have many collections.dependent nullify
- have many credits.dependent restrict with error
- have many billboards.dependent destroy
- have many listings.dependent destroy
- have many notifications.dependent delete all
- have many organization memberships.dependent delete all
- have many profile pins.dependent destroy
- have many unspent credits.class name "Credit"
- have many users.through organization memberships
- validate length of company size.is at most 7
- validate length of cta body markdown.is at most 256
- validate length of cta button text.is at most 20
- validate length of email.is at most 64
- validate length of github username.is at most 50

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: generates a secret if set to empty string

- **Given** set to empty string
- **When** the action is triggered
- **Then** generates a secret

### S-3: generates a secret if set to nil

- **Given** set to nil
- **When** the action is triggered
- **Then** generates a secret

### S-4: rejects names with over 50 characters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects names with over 50 characters

### S-5: accepts names with 50 or less characters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts names with 50 or less characters

### S-6: rejects summaries with over 250 characters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects summaries with over 250 characters

### S-7: accepts summaries with 250 or less characters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts summaries with 250 or less characters

### S-8: accepts hex color codes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts hex color codes

### S-9: rejects color names

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects color names

### S-10: rejects RGB colors

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects RGB colors

### S-11: rejects wrong color format

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects wrong color format

### S-12: accepts properly formatted slug

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts properly formatted slug

### S-13: accepts properly formatted slug with numbers

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts properly formatted slug with numbers

