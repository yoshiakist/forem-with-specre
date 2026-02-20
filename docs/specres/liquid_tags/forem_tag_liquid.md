---
id: "01KHY7Q174YF3J7XEVTC195218"
name: "forem_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/forem_tag.rb
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
- spec/liquid_tags/forem_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `ForemTag` within the liquid_tags domain.

### Behavioral Areas

- **determine_klass**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/forem_tag.rb` -- custom Markdown/Liquid embed rendering
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

### S-1: returns StandardError for Forem link that lacks a LiquidTag

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns StandardError for Forem link that lacks a LiquidTag

### S-2: returns CommentTag if link contains /comment/ (connotes comment url)

- **Given** link contains /comment/ (connotes comment url)
- **When** the action is triggered
- **Then** returns CommentTag

### S-3: returns LinkTag if link is general Forem link

- **Given** link is general Forem link
- **When** the action is triggered
- **Then** returns LinkTag

### S-4: returns OrganizationTag if organization profile link

- **Given** organization profile link
- **When** the action is triggered
- **Then** returns OrganizationTag

### S-5: returns PodcastTag if podcast episode link

- **Given** podcast episode link
- **When** the action is triggered
- **Then** returns PodcastTag

### S-6: returns TagTag if link starts with URL.url/t/

- **Given** link starts with URL.url/t/
- **When** the action is triggered
- **Then** returns TagTag

### S-7: returns UserTag if a user profile link

- **Given** a user profile link
- **When** the action is triggered
- **Then** returns UserTag

