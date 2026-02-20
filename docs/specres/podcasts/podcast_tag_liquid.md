---
id: "01KHY7Q0CJ1VRX66PWVQDAXX0T"
name: "podcast_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/podcast_tag.rb
- spec/liquid_tags/podcast_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `PodcastTag` within the podcasts domain.

### Behavioral Areas

- **when given valid link**: rejects invalid link

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/podcast_tag.rb` -- custom Markdown/Liquid embed rendering


## Scenarios

### S-1: fetches target podcast

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** fetches target podcast

### S-2: raises error if podcast does not exist

- **Given** podcast does not exist
- **When** the action is triggered
- **Then** raises error

### S-3: render properly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** render properly

### S-4: rejects invalid link

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid link

