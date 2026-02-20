---
id: "01KHY7Q0QRETGPDPS20Q1AJBK7"
name: "search_feed_content_simple_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/open_search_controller.rb
- app/controllers/search_controller.rb
- app/controllers/stories/articles_search_controller.rb
- app/errors/search.rb
- app/models/concerns/algolia_searchable.rb
- app/models/concerns/algolia_searchable/searchable_article.rb
- app/models/concerns/algolia_searchable/searchable_comment.rb
- app/models/concerns/algolia_searchable/searchable_organization.rb
- app/models/concerns/algolia_searchable/searchable_podcast_episode.rb
- app/models/concerns/algolia_searchable/searchable_tag.rb
- spec/requests/search/feed_content_simple_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Search::FeedContent` within the search domain.

### Behavioral Areas

- **Search::FeedContent (Simple)**: Ensures correct behavior under the specified conditions
- **GET search/feed_content**: Ensures correct behavior under the specified conditions
- **when the new attributes are included in the serializer**: includes conditional title_finalized_for_feed and title_for_metadata for status articles in the Homepage::ArticleSerializer
- **when Homepage::ArticlesQuery includes type_of attribute**: includes conditional title_finalized_for_feed and title_for_metadata for status articles in the Homepage::ArticleSerializer
- **when testing the methods exist on Article model**: includes conditional title_finalized_for_feed and title_for_metadata for status articles in the Homepage::ArticleSerializer

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/open_search_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/search_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/stories/articles_search_controller.rb` -- HTTP request routing and response handling
- `app/errors/search.rb`
- **Model layer**: `app/models/concerns/algolia_searchable.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_article.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_comment.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_organization.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_podcast_episode.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_tag.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: includes conditional title_finalized_for_feed and title_for_metadata for status ...

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes conditional title_finalized_for_feed and title_for_metadata for status articles in the Homepage::ArticleSerializer

### S-2: includes type_of in the ATTRIBUTES list

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes type_of in the ATTRIBUTES list

### S-3: responds to title_finalized_for_feed

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds to title_finalized_for_feed

### S-4: responds to title_for_metadata

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds to title_for_metadata

### S-5: responds to title_finalized

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds to title_finalized

