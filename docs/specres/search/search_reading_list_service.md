---
id: "01KHY7Q0R1ET5F3VP1JCTYGY93"
name: "search_reading_list_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/serializers/search/reading_list_article_serializer.rb
- app/services/search/reading_list.rb
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
- spec/services/search/reading_list_spec.rb

## Functional Overview

This specification defines the expected behavior of `Search::ReadingList` within the search domain.

### Behavioral Areas

- **::search_documents**: Ensures correct behavior under the specified conditions
- **with an article added to a reading list then unpublished**: returns an empty result without a user
- **when describing the result format**: returns an empty result without a user
- **when filtering by statuses**: selects items with the requested statuses and articles tags
- **when filtering by tags**: selects items belonging to an article with all the requested tags
- **when filtering by statuses and tags**: selects items belonging to an article with all the requested tags
- **when searching for a term**: selects items with the requested status belonging to articles matching the term
- **when searching for a term and filtering by statuses**: selects items with the requested statuses and articles tags

### Implementation Architecture

The behavior is implemented across the following layers:

- **Serializer**: `app/serializers/search/reading_list_article_serializer.rb` -- API response formatting and data transformation
- **Service layer**: `app/services/search/reading_list.rb` -- business logic orchestration and domain operations
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

### S-1: returns an empty result without a user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an empty result without a user

### S-2: does not include an article not in the reading list

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not include an article not in the reading list

### S-3: does not return an article belonging to another user

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not return an article belonging to another user

### S-4: returns results of articles in the reading list

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns results of articles in the reading list

### S-5: returns the total count of the articles in the reading list

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the total count of the articles in the reading list

### S-6: does not include the unpublished article

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not include the unpublished article

### S-7: returns the correct attributes for the result

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct attributes for the result

### S-8: returns the correct attributes for a reading list item

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct attributes for a reading list item

### S-9: returns the correct attributes for a reading list item

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct attributes for a reading list item

### S-10: returns the correct attributes for a reading list item

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct attributes for a reading list item

### S-11: returns confirmed items by default

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns confirmed items by default

### S-12: returns valid items by default

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns valid items by default

