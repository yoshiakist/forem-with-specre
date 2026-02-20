---
id: "01KHY7Q198F7KC3AFCP8B9SXQF"
name: "spotify_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/spotify_tag.rb
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
- spec/liquid_tags/spotify_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `SpotifyTag` within the liquid_tags domain.

### Behavioral Areas

- **link**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/spotify_tag.rb` -- custom Markdown/Liquid embed rendering
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

### S-1: generates the proper iframe if the uri is valid

- **Given** the uri is valid
- **When** the action is triggered
- **Then** generates the proper iframe

### S-2: does not raise an error if the uri is valid

- **Given** the uri is valid
- **When** the action is triggered
- **Then** does not raise an error

### S-3: does not raise an error if the playlist uri is valid

- **Given** the playlist uri is valid
- **When** the action is triggered
- **Then** does not raise an error

### S-4: does not raise an error for a legacy playlist URI

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not raise an error for a legacy playlist URI

### S-5: raises an error if the uri is invalid

- **Given** the uri is invalid
- **When** the action is triggered
- **Then** raises an error

