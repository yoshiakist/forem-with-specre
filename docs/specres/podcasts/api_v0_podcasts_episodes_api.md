---
id: "01KHY7Q0D0HSQYXEZSTF7MS1D8"
name: "api_v0_podcasts_episodes_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/api/v0/podcast_episodes_controller.rb
- spec/requests/api/v0/podcasts_episodes_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Api::V0::PodcastEpisodes"` within the podcasts domain.

### Behavioral Areas

- **Api::V0::PodcastEpisodes**: Ensures correct behavior under the specified conditions
- **GET /api/podcast_episodes**: Ensures correct behavior under the specified conditions
- **when given a username parameter**: returns only podcasts for a given username

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/api/v0/podcast_episodes_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns json response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns json response

### S-2: does not return unreachable podcasts

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not return unreachable podcasts

### S-3: does not return reachable podcast episodes belonging to unpublished podcasts

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not return reachable podcast episodes belonging to unpublished podcasts

### S-4: returns correct attributes for an episode

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns correct attributes for an episode

### S-5: returns the episode

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the episode

### S-6: returns episodes in reverse publishing order

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns episodes in reverse publishing order

### S-7: supports pagination

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** supports pagination

### S-8: respects API_PER_PAGE_MAX limit set in ENV variable

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** respects API_PER_PAGE_MAX limit set in ENV variable

### S-9: sets the correct edge caching surrogate key for all tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sets the correct edge caching surrogate key for all tags

### S-10: returns only podcasts for a given username

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only podcasts for a given username

### S-11: returns not found if the episode belongs to an unpublished podcast

- **Given** the episode belongs to an unpublished podcast
- **When** the action is triggered
- **Then** returns not found

### S-12: returns not found if the podcast episode is unreachable

- **Given** the podcast episode is unreachable
- **When** the action is triggered
- **Then** returns not found

