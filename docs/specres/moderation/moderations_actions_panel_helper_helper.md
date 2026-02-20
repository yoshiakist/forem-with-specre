---
id: "01KHY7Q0MT9SBK397EN7M9914C"
name: "moderations_actions_panel_helper_helper"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/helpers/moderations/actions_panel_helper.rb
- app/controllers/moderations_controller.rb
- app/services/moderations/article_fetcher_service.rb
- spec/helpers/moderations/actions_panel_helper_spec.rb

## Functional Overview

This specification defines the expected behavior of `Actions_Panel_Helper` within the moderation domain.

### Behavioral Areas

- **last_adjusted_by_admin?**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **View helper**: `app/helpers/moderations/actions_panel_helper.rb` -- shared view utility methods
- **Controller layer**: `app/controllers/moderations_controller.rb` -- HTTP request routing and response handling
- **Service layer**: `app/services/moderations/article_fetcher_service.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns false if the last adjustment was made by a non-admin

- **Given** the last adjustment was made by a non-admin
- **When** the action is triggered
- **Then** returns false

### S-2: returns true if the last adjustment was made by any admin

- **Given** the last adjustment was made by any admin
- **When** the action is triggered
- **Then** returns true

