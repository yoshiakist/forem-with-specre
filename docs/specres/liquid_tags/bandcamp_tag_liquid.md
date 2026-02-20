---
id: "01KHY7Q16BP72JQMP4NM45HYAH"
name: "bandcamp_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/bandcamp_tag.rb
- app/controllers/liquid_tags_controller.rb
- app/errors/liquid_tags.rb
- app/liquid_tags/asciinema_tag.rb
- app/liquid_tags/blogcast_tag.rb
- app/liquid_tags/bluesky_tag.rb
- app/liquid_tags/card_tag.rb
- app/liquid_tags/cloud_run_tag.rb
- app/liquid_tags/codepen_tag.rb
- app/liquid_tags/codesandbox_tag.rb
- app/liquid_tags/comment_tag.rb
- spec/liquid_tags/bandcamp_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `BandcampTag` within the liquid_tags domain.

### Behavioral Areas

- **render**: renders the Bandcamp album player iframe
- **with a valid Bandcamp album URL**: renders the Bandcamp album player iframe
- **with a valid Bandcamp track URL**: renders the Bandcamp album player iframe
- **with an invalid Bandcamp URL format**: renders the Bandcamp album player iframe
- **with a non-Bandcamp URL**: renders the Bandcamp track player iframe with album and track ID
- **when fetching page data fails**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/bandcamp_tag.rb` -- custom Markdown/Liquid embed rendering
- **Controller layer**: `app/controllers/liquid_tags_controller.rb` -- HTTP request routing and response handling
- `app/errors/liquid_tags.rb`
- **Liquid tag**: `app/liquid_tags/asciinema_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/blogcast_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/bluesky_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/card_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/cloud_run_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/codepen_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/codesandbox_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/comment_tag.rb` -- custom Markdown/Liquid embed rendering


## Scenarios

### S-1: renders the Bandcamp album player iframe

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the Bandcamp album player iframe

### S-2: renders the Bandcamp track player iframe with album and track ID

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the Bandcamp track player iframe with album and track ID

### S-3: returns an error message

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an error message

### S-4: returns an error message

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an error message

### S-5: returns an error message

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an error message

