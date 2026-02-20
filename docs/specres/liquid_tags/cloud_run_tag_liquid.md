---
id: "01KHY7Q16NNC2WB17X8TJ5BBT3"
name: "cloud_run_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/cloud_run_tag.rb
- app/controllers/liquid_tags_controller.rb
- app/errors/liquid_tags.rb
- app/liquid_tags/asciinema_tag.rb
- app/liquid_tags/bandcamp_tag.rb
- app/liquid_tags/blogcast_tag.rb
- app/liquid_tags/bluesky_tag.rb
- app/liquid_tags/card_tag.rb
- app/liquid_tags/codepen_tag.rb
- app/liquid_tags/codesandbox_tag.rb
- app/liquid_tags/comment_tag.rb
- spec/liquid_tags/cloud_run_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `CloudRunTag` within the liquid_tags domain.

### Behavioral Areas

- **url**: Ensures correct behavior under the specified conditions
- **embed tag integration**: works with embed tag

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/cloud_run_tag.rb` -- custom Markdown/Liquid embed rendering
- **Controller layer**: `app/controllers/liquid_tags_controller.rb` -- HTTP request routing and response handling
- `app/errors/liquid_tags.rb`
- **Liquid tag**: `app/liquid_tags/asciinema_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/bandcamp_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/blogcast_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/bluesky_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/card_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/codepen_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/codesandbox_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/comment_tag.rb` -- custom Markdown/Liquid embed rendering


## Scenarios

### S-1: accepts valid Cloud Run URL with trailing slash

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts valid Cloud Run URL with trailing slash

### S-2: accepts valid Cloud Run URL without trailing slash

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts valid Cloud Run URL without trailing slash

### S-3: accepts valid Cloud Run URL with region in hostname

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts valid Cloud Run URL with region in hostname

### S-4: accepts simple Cloud Run URL format

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts simple Cloud Run URL format

### S-5: renders iframe with proper attributes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders iframe with proper attributes

### S-6: raises an error for invalid Cloud Run URL

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an error for invalid Cloud Run URL

### S-7: raises an error for invalid format

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an error for invalid format

### S-8: raises an error for non-Cloud Run URLs

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises an error for non-Cloud Run URLs

### S-9: works with embed tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** works with embed tag

### S-10: renders iframe with proper attributes via embed tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders iframe with proper attributes via embed tag

