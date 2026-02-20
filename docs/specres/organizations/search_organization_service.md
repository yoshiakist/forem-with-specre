---
id: "01KHY7Q0JE6TX7GM2WY4HACZZF"
name: "search_organization_service"
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
- spec/services/search/organization_spec.rb

## Functional Overview

This specification defines the expected behavior of `Search::Organization` within the organizations domain.

### Behavioral Areas

- **::search_documents**: Ensures correct behavior under the specified conditions
- **when searching for a term**: Ensures correct behavior under the specified conditions

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

### S-1: returns an empty result if there are no orgnizations

- **Given** there are no orgnizations
- **When** the action is triggered
- **Then** returns an empty result

### S-2: matches against the organization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** matches against the organization

