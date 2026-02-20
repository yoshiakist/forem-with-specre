---
id: "01KHY7Q16GXAFGXM33JT2XMZZX"
name: "bluesky_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/bluesky_tag.rb
- app/controllers/liquid_tags_controller.rb
- app/errors/liquid_tags.rb
- app/liquid_tags/asciinema_tag.rb
- app/liquid_tags/bandcamp_tag.rb
- app/liquid_tags/blogcast_tag.rb
- app/liquid_tags/card_tag.rb
- app/liquid_tags/cloud_run_tag.rb
- app/liquid_tags/codepen_tag.rb
- app/liquid_tags/codesandbox_tag.rb
- app/liquid_tags/comment_tag.rb
- spec/liquid_tags/bluesky_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `BlueskyTag` within the liquid_tags domain.

### Behavioral Areas

- **render**: renders the Bluesky embed for a valid URL

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/bluesky_tag.rb` -- custom Markdown/Liquid embed rendering
- **Controller layer**: `app/controllers/liquid_tags_controller.rb` -- HTTP request routing and response handling
- `app/errors/liquid_tags.rb`
- **Liquid tag**: `app/liquid_tags/asciinema_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/bandcamp_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/blogcast_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/card_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/cloud_run_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/codepen_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/codesandbox_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/comment_tag.rb` -- custom Markdown/Liquid embed rendering


## Scenarios

### S-1: renders the Bluesky embed for a valid URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the Bluesky embed for a valid URL

### S-2: renders the Bluesky embed for a valid AT-URI

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the Bluesky embed for a valid AT-URI

### S-3: rejects invalid inputs

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid inputs

### S-4: accepts a valid URL without raising errors

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid URL without raising errors

