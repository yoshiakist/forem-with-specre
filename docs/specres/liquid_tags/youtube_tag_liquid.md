---
id: "01KHY7Q1AAZBKMTGD8M48W2GAT"
name: "youtube_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/youtube_tag.rb
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
- spec/liquid_tags/youtube_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `YoutubeTag` within the liquid_tags domain.

### Behavioral Areas

- **id**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/youtube_tag.rb` -- custom Markdown/Liquid embed rendering
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

### S-1: accepts a short URL

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a short URL

### S-2: accepts a short URL with 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a short URL with 

### S-3: accepts a short URL with 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a short URL with 

### S-4: accepts a short URL with both 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a short URL with both 

### S-5: accepts a full URL with 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a full URL with 

### S-6: accepts a full URL with 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a full URL with 

### S-7: accepts a full URL with 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a full URL with 

### S-8: accepts an ID only

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts an ID only

### S-9: raises an error for invalid IDs

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an error for invalid IDs

### S-10: raises an error for invalid URLs

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an error for invalid URLs

