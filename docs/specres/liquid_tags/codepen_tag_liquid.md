---
id: "01KHY7Q16RRM8VS60JYZ77CRNX"
name: "codepen_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/codepen_tag.rb
- app/controllers/liquid_tags_controller.rb
- app/errors/liquid_tags.rb
- app/liquid_tags/asciinema_tag.rb
- app/liquid_tags/bandcamp_tag.rb
- app/liquid_tags/blogcast_tag.rb
- app/liquid_tags/bluesky_tag.rb
- app/liquid_tags/card_tag.rb
- app/liquid_tags/cloud_run_tag.rb
- app/liquid_tags/codesandbox_tag.rb
- app/liquid_tags/comment_tag.rb
- spec/liquid_tags/codepen_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `CodepenTag` within the liquid_tags domain.

### Behavioral Areas

- **link**: accepts codepen link

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/codepen_tag.rb` -- custom Markdown/Liquid embed rendering
- **Controller layer**: `app/controllers/liquid_tags_controller.rb` -- HTTP request routing and response handling
- `app/errors/liquid_tags.rb`
- **Liquid tag**: `app/liquid_tags/asciinema_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/bandcamp_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/blogcast_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/bluesky_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/card_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/cloud_run_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/codesandbox_tag.rb` -- custom Markdown/Liquid embed rendering
- **Liquid tag**: `app/liquid_tags/comment_tag.rb` -- custom Markdown/Liquid embed rendering


## Scenarios

### S-1: accepts codepen link

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts codepen link

### S-2: accepts codepen private link

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts codepen private link

### S-3: accepts codepen link with a / at the end

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts codepen link with a / at the end

### S-4: accepts codepen team link

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts codepen team link

### S-5: accepts codepen team private link

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts codepen team private link

### S-6: accepts codepen link with an underscore in the username

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts codepen link with an underscore in the username

### S-7: rejects invalid codepen link

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid codepen link

### S-8: rejects codepen link with more than 30 characters in the username

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects codepen link with more than 30 characters in the username

### S-9: accepts codepen link with a default-tab parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts codepen link with a default-tab parameter

### S-10: accepts codepen link with a theme-id parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts codepen link with a theme-id parameter

### S-11: accepts codepen link with pen/preview in the url

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts codepen link with pen/preview in the url

### S-12: accepts codepen link with embed path in the url

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** accepts codepen link with embed path in the url

