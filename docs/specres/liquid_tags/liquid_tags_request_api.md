---
id: "01KHY7Q1AFQ0GH49KHV8BXM866"
name: "liquid_tags_request_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/liquid_tags_controller.rb
- app/errors/liquid_tags.rb
- app/liquid_tags/asciinema_tag.rb
- app/liquid_tags/bandcamp_tag.rb
- app/liquid_tags/blogcast_tag.rb
- app/liquid_tags/bluesky_tag.rb
- spec/requests/liquid_tags_request_spec.rb

## Functional Overview

This specification defines the expected behavior of `"LiquidTags"` within the liquid_tags domain.

### Behavioral Areas

- **LiquidTags**: Ensures correct behavior under the specified conditions
- **GET /liquid_tags**: Ensures correct behavior under the specified conditions
- **when not signed in do**: Ensures correct behavior under the specified conditions
- **when signed in**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/liquid_tags_controller.rb` -- HTTP request routing and response handling
- `app/errors/liquid_tags.rb`
- **Liquid tag**: `app/liquid_tags/asciinema_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/bandcamp_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/blogcast_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/bluesky_tag.rb` -- custom Markdown/Liquid embed rendering


## Scenarios

### S-1: returns a list of all custom Liquid tags

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a list of all custom Liquid tags

### S-2: returns an array of all custom Liquid tags

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an array of all custom Liquid tags

