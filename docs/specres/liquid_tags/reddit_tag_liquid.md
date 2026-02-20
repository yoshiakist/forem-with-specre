---
id: "01KHY7Q18SZ6XS1KAFRD8V9NW8"
name: "reddit_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/reddit_tag.rb
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
- spec/liquid_tags/reddit_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `RedditTag` within the liquid_tags domain.

### Behavioral Areas

- **when it is an image post**: Ensures correct behavior under the specified conditions
- **render**: renders reddit content
- **when it is a text post**: Ensures correct behavior under the specified conditions
- **render**: renders reddit content

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/reddit_tag.rb` -- custom Markdown/Liquid embed rendering
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

### S-1: renders reddit content

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders reddit content

### S-2: renders reddit content

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders reddit content

