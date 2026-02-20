---
id: "01KHY7Q028DXG9C36QQQSCCX39"
name: "podcasts_user_visits_podcast_episode_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/users/delete_podcasts.rb
- spec/system/podcasts/user_visits_podcast_episode_spec.rb

## Functional Overview

This specification defines the expected behavior of `"User` within the users domain.

### Behavioral Areas

- **User visits podcast show page**: see the new comment box on the page
- **when mobile apps read the podcast episode metadata**: renders the Episode & Podcast data
- **when episode may not be playable**: renders the Episode & Podcast data
- **when podcast has another status_notice (just in case)**: renders the Episode & Podcast data
- **when podcast has publish_at field**: renders the Episode & Podcast data
- **when there are existing comments**: displays status when episode is not reachable by https

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/users/delete_podcasts.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-2: they see the content of the hero

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** they see the content of the hero

### S-3: see the new comment box on the page

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** see the new comment box on the page

### S-4: renders the Episode & Podcast data

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the Episode & Podcast data

### S-5: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-6: displays status when episode is not reachable by https

- **Given** the system is in a standard operational state
- **When** episode is not reachable by https
- **Then** displays status

### S-7: doesn

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** doesn

### S-8: sees published at

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sees published at

### S-9: sees the comments

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sees the comments

