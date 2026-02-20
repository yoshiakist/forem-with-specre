---
id: "01KHY7Q16TBY5SYM8RZPF7ZE1J"
name: "codesandbox_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/codesandbox_tag.rb
- app/controllers/liquid_tags_controller.rb
- app/errors/liquid_tags.rb
- app/liquid_tags/asciinema_tag.rb
- app/liquid_tags/bandcamp_tag.rb
- app/liquid_tags/blogcast_tag.rb
- app/liquid_tags/bluesky_tag.rb
- app/liquid_tags/card_tag.rb
- app/liquid_tags/cloud_run_tag.rb
- app/liquid_tags/codepen_tag.rb
- app/liquid_tags/comment_tag.rb
- spec/liquid_tags/codesandbox_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `CodesandboxTag` within the liquid_tags domain.

### Behavioral Areas

- **id**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/codesandbox_tag.rb` -- custom Markdown/Liquid embed rendering
- **Controller layer**: `app/controllers/liquid_tags_controller.rb` -- HTTP request routing and response handling
- `app/errors/liquid_tags.rb`
- **Liquid tag**: `app/liquid_tags/asciinema_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/bandcamp_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/blogcast_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/bluesky_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/card_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/cloud_run_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/codepen_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/comment_tag.rb` -- custom Markdown/Liquid embed rendering


## Scenarios

### S-1: accepts a valid id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid id

### S-2: accepts a valid id with file

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid id with file

### S-3: accepts a valid id with initialpath

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid id with initialpath

### S-4: accepts a valid id with module

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid id with module

### S-5: accepts a valid id with view

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid id with view

### S-6: accepts a valid id with runonclick

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid id with runonclick

### S-7: accepts a valid id with initialpath and module

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid id with initialpath and module

### S-8: accepts a valid id with initialpath and view

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid id with initialpath and view

### S-9: accepts a valid id with initialpath and runonclick

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid id with initialpath and runonclick

### S-10: accepts a valid id with runonclick and module

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid id with runonclick and module

### S-11: accepts a valid id with runonclick and view

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid id with runonclick and view

### S-12: accepts a valid id with initialpath and module and runonclick

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a valid id with initialpath and module and runonclick

