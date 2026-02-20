---
id: "01KHY7Q19B1K71FPV1WNF2JJVJ"
name: "stackblitz_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/stackblitz_tag.rb
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
- spec/liquid_tags/stackblitz_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `StackblitzTag` within the liquid_tags domain.

### Behavioral Areas

- **id**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/stackblitz_tag.rb` -- custom Markdown/Liquid embed rendering
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

### S-1: renders iframe

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders iframe

### S-2: rejects invalid stackblitz id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid stackblitz id

### S-3: parses stackblitz id with a view parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** parses stackblitz id with a view parameter

### S-4: parses stackblitz id with a file parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** parses stackblitz id with a file parameter

### S-5: parses stackblitz id with a view and file parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** parses stackblitz id with a view and file parameter

### S-6: parses stackblitz id with an embed parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** parses stackblitz id with an embed parameter

### S-7: parses stackblitz id with a hideNavigation parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** parses stackblitz id with a hideNavigation parameter

### S-8: parses stackblitz id with a theme parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** parses stackblitz id with a theme parameter

### S-9: parses stackblitz id with a ctl parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** parses stackblitz id with a ctl parameter

### S-10: parses stackblitz id with a devtoolsheight parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** parses stackblitz id with a devtoolsheight parameter

### S-11: parses stackblitz id with a hidedevtools parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** parses stackblitz id with a hidedevtools parameter

### S-12: parses stackblitz id with a initialpath parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** parses stackblitz id with a initialpath parameter

