---
id: "01KHY7Q180N60FFC3R1GQJ3Q1N"
name: "link_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/link_tag.rb
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
- spec/liquid_tags/link_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `LinkTag` within the liquid_tags domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/link_tag.rb` -- custom Markdown/Liquid embed rendering
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

### S-1: can use 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** can use 

### S-2: does not raise an error when invalid

- **Given** the system is in a standard operational state
- **When** invalid
- **Then** does not raise an error

### S-3: renders a proper link tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders a proper link tag

### S-4: also tries to look for article by organization if failed to find by username

- **Given** failed to find by username
- **When** the action is triggered
- **Then** also tries to look for article by organization

### S-5: renders with a leading slash

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders with a leading slash

### S-6: renders with a trailing slash

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders with a trailing slash

### S-7: renders with both leading and trailing slashes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders with both leading and trailing slashes

### S-8: renders with a full link

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders with a full link

### S-9: raise error when url belongs to different domain

- **Given** the system is in a standard operational state
- **When** url belongs to different domain
- **Then** raise error

### S-10: does not raise error if a subforem with domain exists

- **Given** a subforem with domain exists
- **When** the action is triggered
- **Then** does not raise error

### S-11: renders with a full link with a trailing slash

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders with a full link with a trailing slash

### S-12: renders with missing article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders with missing article

