---
id: "01KHY7Q16Z3M9TDM7CK7WS7410"
name: "details_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/details_tag.rb
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
- spec/liquid_tags/details_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `DetailsTag` within the liquid_tags domain.

### Behavioral Areas

- **render**: Ensures correct behavior under the specified conditions
- **when content has simple text**: Ensures correct behavior under the specified conditions
- **when content has a strong tag**: accepts a strong tag
- **when content has a link tag**: accepts a link tag
- **when content has a h2 tag**: Ensures correct behavior under the specified conditions
- **when content has a list**: accepts a list tag
- **when content has an img tag**: Ensures correct behavior under the specified conditions
- **when content has a code tag**: accepts a code tag

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/details_tag.rb` -- custom Markdown/Liquid embed rendering
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

### S-1: generates proper details div with summary

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates proper details div with summary

### S-2: accepts a strong tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a strong tag

### S-3: accepts a link tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a link tag

### S-4: accepts a h2 tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a h2 tag

### S-5: accepts a list tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a list tag

### S-6: accepts an img tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts an img tag

### S-7: accepts a code tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts a code tag

### S-8: removes a div tag

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes a div tag

### S-9: removes unpermitted tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes unpermitted tags

### S-10: removes an unpermitted attribute

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** removes an unpermitted attribute

### S-11: accepts these tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts these tags

