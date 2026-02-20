---
id: "01KHY7Q0CNDR5A72G8AHQSZCY4"
name: "podcast_episode_appearance_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/podcast_episode_appearance.rb
- app/models/concerns/algolia_searchable/searchable_podcast_episode.rb
- app/models/podcast.rb
- app/models/podcast_episode.rb
- app/models/podcast_ownership.rb
- spec/models/podcast_episode_appearance_spec.rb

## Functional Overview

This specification defines the expected behavior of `PodcastEpisodeAppearance` within the podcasts domain.

### Behavioral Areas

- **validations**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/podcast_episode_appearance.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_podcast_episode.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/podcast.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/podcast_episode.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/podcast_ownership.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- belong to user.inverse of podcast episode appearances
- belong to podcast episode
- validate presence of role
- validate uniqueness of podcast episode id.scoped to user id

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

