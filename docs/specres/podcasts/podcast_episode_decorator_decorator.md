---
id: "01KHY7Q0CGZCFZMYJ27ZF7ZCN3"
name: "podcast_episode_decorator_decorator"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/decorators/podcast_episode_decorator.rb
- spec/decorators/podcast_episode_decorator_spec.rb

## Functional Overview

This specification defines the expected behavior of `PodcastEpisodeDecorator` within the podcasts domain.

### Behavioral Areas

- **with serialization**: returns the correct date for a publication within a different year
- **cached_tag_list_array**: Ensures correct behavior under the specified conditions
- **readable_publish_date**: Ensures correct behavior under the specified conditions
- **published_timestamp**: Ensures correct behavior under the specified conditions
- **mobile_player_metadata**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Decorator**: `app/decorators/podcast_episode_decorator.rb` -- presentation logic and view-model enrichment


## Scenarios

### S-1: serializes both the decorated object IDs and decorated methods

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** serializes both the decorated object IDs and decorated methods

### S-2: serializes collections of decorated objects

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** serializes collections of decorated objects

### S-3: returns no tags if the tag list is empty

- **Given** the tag list is empty
- **When** the action is triggered
- **Then** returns no tags

### S-4: returns tag list

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns tag list

### S-5: returns empty string if the episode does not have a published_at

- **Given** the episode does not have a published_at
- **When** the action is triggered
- **Then** returns empty string

### S-6: returns the correct date for a same year publication

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct date for a same year publication

### S-7: returns the correct date for a publication within a different year

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct date for a publication within a different year

### S-8: returns empty string if the episode does not have a published_at

- **Given** the episode does not have a published_at
- **When** the action is triggered
- **Then** returns empty string

### S-9: returns the correct date for a published episode

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct date for a published episode

### S-10: responds with a hash with metadata used in native mobile players

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds with a hash with metadata used in native mobile players

