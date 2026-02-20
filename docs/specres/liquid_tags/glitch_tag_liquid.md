---
id: "01KHY7Q17HYMATYWQ4ECG7EYHX"
name: "glitch_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/glitch_tag.rb
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
- spec/liquid_tags/glitch_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `GlitchTag` within the liquid_tags domain.

### Behavioral Areas

- **id**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/glitch_tag.rb` -- custom Markdown/Liquid embed rendering
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

### S-1: accepts a valid id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid id

### S-2: does not accept double quotes

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not accept double quotes

### S-3: handles 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles 

### S-4: handles 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles 

### S-5: handles 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles 

### S-6: handles 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles 

### S-7: handles 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles 

### S-8: handles 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles 

### S-9: handles complex case

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles complex case

### S-10: 'app

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** 'app

### S-11: removes the tilde prefix of ids

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes the tilde prefix of ids

