---
id: "01KHY7Q168EAM588HFQKSG16P9"
name: "asciinema_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/asciinema_tag.rb
- app/controllers/liquid_tags_controller.rb
- app/errors/liquid_tags.rb
- app/liquid_tags/bandcamp_tag.rb
- app/liquid_tags/blogcast_tag.rb
- app/liquid_tags/bluesky_tag.rb
- app/liquid_tags/card_tag.rb
- app/liquid_tags/cloud_run_tag.rb
- app/liquid_tags/codepen_tag.rb
- app/liquid_tags/codesandbox_tag.rb
- app/liquid_tags/comment_tag.rb
- spec/liquid_tags/asciinema_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `AsciinemaTag` within the liquid_tags domain.

### Behavioral Areas

- **id**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/asciinema_tag.rb` -- custom Markdown/Liquid embed rendering
- **Controller layer**: `app/controllers/liquid_tags_controller.rb` -- HTTP request routing and response handling
- `app/errors/liquid_tags.rb`
- **Liquid tag**: `app/liquid_tags/bandcamp_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/blogcast_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/bluesky_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/card_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/cloud_run_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/codepen_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/codesandbox_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/comment_tag.rb` -- custom Markdown/Liquid embed rendering


## Scenarios

### S-1: rejects invalid ids

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid ids

### S-2: accepts a valid numeric id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid numeric id

### S-3: accepts a valid base64 URL id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid base64 URL id

### S-4: rejects ids with invalid characters

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects ids with invalid characters

### S-5: rejects invalid URLs

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid URLs

### S-6: accepts a valid URL with numeric id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid URL with numeric id

### S-7: accepts a valid URL with base64 URL id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid URL with base64 URL id

