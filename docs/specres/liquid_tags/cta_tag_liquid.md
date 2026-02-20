---
id: "01KHY7Q16XT4NB6ZXCV7MYBWVW"
name: "cta_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/cta_tag.rb
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
- spec/liquid_tags/cta_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `CtaTag` within the liquid_tags domain.

### Behavioral Areas

- **render**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/cta_tag.rb` -- custom Markdown/Liquid embed rendering
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

### S-1: contains the correct static attributes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains the correct static attributes

### S-2: generates the correct href attribute

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates the correct href attribute

### S-3: contains the correct description

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** contains the correct description

### S-4: limits the description to 128 characters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** limits the description to 128 characters

### S-5: strips all tags from the description

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** strips all tags from the description

