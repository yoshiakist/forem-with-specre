---
id: "01KHY7Q18ACWNBX5TDVN3E7G5G"
name: "mux_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/mux_tag.rb
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
- spec/liquid_tags/mux_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `MuxTag` within the liquid_tags domain.

### Behavioral Areas

- **rendering**: extracts video ID correctly from URL through rendering
- **UnifiedEmbed integration**: is registered with UnifiedEmbed

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/mux_tag.rb` -- custom Markdown/Liquid embed rendering
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

### S-1: returns Mux embed for valid Mux player URL

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns Mux embed for valid Mux player URL

### S-2: returns Mux embed for valid Mux player URL with query parameters

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns Mux embed for valid Mux player URL with query parameters

### S-3: handles different video ID formats

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles different video ID formats

### S-4: extracts video ID correctly from URL through rendering

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** extracts video ID correctly from URL through rendering

### S-5: handles URLs with query parameters through rendering

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles URLs with query parameters through rendering

### S-6: is registered with UnifiedEmbed

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** is registered with UnifiedEmbed

### S-7: works with embed tag syntax

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** works with embed tag syntax

### S-8: does not match non-Mux URLs

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not match non-Mux URLs

