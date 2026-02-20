---
id: "01KHY7Q1790Z2YJYZ56E24Z646"
name: "git_pitch_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/git_pitch_tag.rb
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
- spec/liquid_tags/git_pitch_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `GitPitchTag` within the liquid_tags domain.

### Behavioral Areas

- **link**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/git_pitch_tag.rb` -- custom Markdown/Liquid embed rendering
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

### S-1: rejects invalid gitpitch url

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid gitpitch url

### S-2: accepts valid gitpitch url

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts valid gitpitch url

