---
id: "01KHY7Q19K3T435K5XD2YF421F"
name: "survey_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/survey_tag.rb
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
- spec/liquid_tags/survey_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `SurveyTag` within the liquid_tags domain.

### Behavioral Areas

- **.user_authorization_method_name**: Ensures correct behavior under the specified conditions
- **render**: renders survey with polls

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/survey_tag.rb` -- custom Markdown/Liquid embed rendering
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

### S-1: Data integrity and associations

The model enforces the following constraints:

- eq nil

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: renders survey with polls

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders survey with polls

### S-3: renders polls with supplementary text

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders polls with supplementary text

### S-4: renders scale polls with supplementary text on first and last options

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders scale polls with supplementary text on first and last options

### S-5: renders scale polls with vertical supplementary text within scale value buttons

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders scale polls with vertical supplementary text within scale value buttons

### S-6: allows non-admin users in non-article contexts

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows non-admin users in non-article contexts

