---
id: "01KHY7Q17PSDG0FFADNPP1YWZC"
name: "js_fiddle_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/js_fiddle_tag.rb
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
- spec/liquid_tags/js_fiddle_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `JsFiddleTag` within the liquid_tags domain.

### Behavioral Areas

- **link**: accepts jsfiddle link

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/js_fiddle_tag.rb` -- custom Markdown/Liquid embed rendering
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

### S-1: accepts jsfiddle link

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts jsfiddle link

### S-2: accepts jsfiddle link with a / at the end

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts jsfiddle link with a / at the end

### S-3: rejects invalid jsfiddle link

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid jsfiddle link

### S-4: accepts jsfiddle link with a custom-tab parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts jsfiddle link with a custom-tab parameter

### S-5: rejects XSS attempts

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects XSS attempts

