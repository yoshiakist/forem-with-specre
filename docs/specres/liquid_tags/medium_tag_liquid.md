---
id: "01KHY7Q188Z0GTFZ4HHHYGAWCT"
name: "medium_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/medium_tag.rb
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
- spec/liquid_tags/medium_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `MediumTag` within the liquid_tags domain.

### Behavioral Areas

- **when given valid medium url**: renders link to Medium profile

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/medium_tag.rb` -- custom Markdown/Liquid embed rendering
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

### S-1: renders the proper author name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper author name

### S-2: renders user image html

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders user image html

### S-3: renders article reading time

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders article reading time

### S-4: renders link to Medium profile

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders link to Medium profile

### S-5: raises an error when invalid

- **Given** the system is in a standard operational state
- **When** invalid
- **Then** raises an error

