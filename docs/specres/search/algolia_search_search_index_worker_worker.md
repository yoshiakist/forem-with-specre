---
id: "01KHY7Q0R838SJ4ZN5WR1DQYEG"
name: "algolia_search_search_index_worker_worker"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/algolia_search/search_index_worker.rb
- app/models/concerns/algolia_searchable.rb
- app/models/concerns/algolia_searchable/searchable_article.rb
- app/models/concerns/algolia_searchable/searchable_comment.rb
- app/models/concerns/algolia_searchable/searchable_organization.rb
- app/models/concerns/algolia_searchable/searchable_podcast_episode.rb
- app/models/concerns/algolia_searchable/searchable_tag.rb
- app/models/concerns/algolia_searchable/searchable_user.rb
- spec/workers/algolia_search/search_index_worker_spec.rb

## Functional Overview

This specification defines the expected behavior of `AlgoliaSearch::SearchIndexWorker` within the search domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- **Background worker**: `app/workers/algolia_search/search_index_worker.rb` -- asynchronous job processing
- **Model layer**: `app/models/concerns/algolia_searchable.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_article.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_comment.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_organization.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_podcast_episode.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_tag.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_user.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: remove the record from Algolia if record is deleted

- **Given** record is deleted
- **When** the action is triggered
- **Then** remove the record from Algolia

### S-2: index the record in Algolia if record is created

- **Given** record is created
- **When** the action is triggered
- **Then** index the record in Algolia

