---
id: "01KHY7Q17SFMDGT3FXN9QVMY6K"
name: "jsitor_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/jsitor_tag.rb
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
- spec/liquid_tags/jsitor_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `JsitorTag` within the liquid_tags domain.

### Behavioral Areas

- **link**: parses the link with spaces before and after

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/jsitor_tag.rb` -- custom Markdown/Liquid embed rendering
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

### S-1: renders jsitor liquid tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders jsitor liquid tag

### S-2: parses the link with spaces before and after

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** parses the link with spaces before and after

### S-3: accepts jsitor link with query params

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts jsitor link with query params

### S-4: accepts jsitor id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts jsitor id

### S-5: accepts jsitor id with parameters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts jsitor id with parameters

### S-6: accepts jsitor link with hyphen id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts jsitor link with hyphen id

### S-7: accepts jsitor id with hyphen

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts jsitor id with hyphen

### S-8: doesnt accepts jsitor link with a / at the end

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesnt accepts jsitor link with a / at the end

### S-9: does not accept invalid links

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not accept invalid links

### S-10: rejects XSS attempts

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects XSS attempts

