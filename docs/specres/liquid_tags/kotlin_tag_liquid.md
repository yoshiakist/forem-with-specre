---
id: "01KHY7Q17Y6YFSY3D1Y3N95T5B"
name: "kotlin_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/kotlin_tag.rb
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
- spec/liquid_tags/kotlin_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `KotlinTag` within the liquid_tags domain.

### Behavioral Areas

- **link**: Ensures correct behavior under the specified conditions
- **with valid Kotlin urls**: generates correct liquid from url without params
- **with invalid Kotlin urls**: generates correct liquid from url without params

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/kotlin_tag.rb` -- custom Markdown/Liquid embed rendering
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

### S-1: generates correct liquid from url without params

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates correct liquid from url without params

### S-2: generates correct liquid from url with one or more params

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** generates correct liquid from url with one or more params

### S-3: returns StandardError from invalid urls

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns StandardError from invalid urls

