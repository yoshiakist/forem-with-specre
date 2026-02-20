---
id: "01KHY7Q1837ACCD722THFTAV7F"
name: "liquid_tag_base_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/liquid_tag_base.rb
- app/controllers/liquid_tags_controller.rb
- app/errors/liquid_tags.rb
- app/liquid_tags/asciinema_tag.rb
- app/liquid_tags/bandcamp_tag.rb
- app/liquid_tags/blogcast_tag.rb
- app/liquid_tags/bluesky_tag.rb
- app/liquid_tags/card_tag.rb
- app/liquid_tags/cloud_run_tag.rb
- app/liquid_tags/codepen_tag.rb
- app/liquid_tags/codesandbox_tag.rb
- spec/liquid_tags/liquid_tag_base_spec.rb

## Functional Overview

This specification defines the expected behavior of `LiquidTagBase` within the liquid_tags domain.

### Behavioral Areas

- **when context includes a policy**: raises an error for invalid contexts
- **when VALID_CONTEXTS are defined**: Ensures correct behavior under the specified conditions
- **when VALID_CONTEXTS aren**: Ensures correct behavior under the specified conditions
- **when .user_authorization_method_name is not nil**: Ensures correct behavior under the specified conditions
- **when .user_authorization_method_name is nil**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/liquid_tag_base.rb` -- custom Markdown/Liquid embed rendering
- **Controller layer**: `app/controllers/liquid_tags_controller.rb` -- HTTP request routing and response handling
- `app/errors/liquid_tags.rb`
- **Liquid tag**: `app/liquid_tags/asciinema_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/bandcamp_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/blogcast_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/bluesky_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/card_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/cloud_run_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/codepen_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/codesandbox_tag.rb` -- custom Markdown/Liquid embed rendering


## Scenarios

### S-1: is used by Pundit for authorization

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is used by Pundit for authorization

### S-2: raises an error for invalid contexts

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an error for invalid contexts

### S-3: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-4: does not validate contexts

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not validate contexts

### S-5: raises an error for invalid roles

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an error for invalid roles

### S-6: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-7: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

