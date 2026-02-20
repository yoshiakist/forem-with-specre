---
id: "01KHY7Q0QV9TQ6VYZSAG3CQPSD"
name: "search_api"
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
- app/models/concerns/algolia_searchable/searchable_user.rb
- app/queries/articles/api_search_query.rb
- app/workers/algolia_search/search_index_worker.rb
- spec/requests/search_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Search"` within the search domain.

### Behavioral Areas

- **Search**: does not call Homepage::FetchArticles when class_name is Article with a search term
- **GET /search/tags**: Ensures correct behavior under the specified conditions
- **GET /search/usernames**: Ensures correct behavior under the specified conditions
- **GET /search/feed_content**: Ensures correct behavior under the specified conditions
- **when searching for articles**: does not call Homepage::FetchArticles when class_name is Article with a search term
- **when searching for comments**: does not call Homepage::FetchArticles when class_name is Article with a search term
- **when using searching for users**: does not call Homepage::FetchArticles when class_name is Article with a search term
- **when using searching for podcasts**: does not call Homepage::FetchArticles when class_name is Article with a search term

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
- **Model layer**: `app/models/concerns/algolia_searchable/searchable_user.rb` -- data persistence, validations, and associations
- **Query object**: `app/queries/articles/api_search_query.rb` -- complex database query encapsulation


## Scenarios

### S-1: returns nothing if there is no name parameter

- **Given** there is no name parameter
- **When** the action is triggered
- **Then** returns nothing

### S-2: finds a tag by a partial name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** finds a tag by a partial name

### S-3: returns nothing if there is no username parameter

- **Given** there is no username parameter
- **When** the action is triggered
- **Then** returns nothing

### S-4: finds a username by a partial username

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** finds a username by a partial username

### S-5: finds a username by a partial name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** finds a username by a partial name

### S-6: does not call Homepage::FetchArticles when class_name is Article with a search t...

- **Given** the system is in a standard operational state
- **When** class_name is Article with a search term
- **Then** does not call Homepage::FetchArticles

### S-7: returns the correct keys

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the correct keys

### S-8: parses published_at correctly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** parses published_at correctly

### S-9: supports the user_id parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** supports the user_id parameter

### S-10: supports the organization_id parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** supports the organization_id parameter

### S-11: supports the tag_names parameter

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** supports the tag_names parameter

### S-12: calls Search::Article without a class_name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calls Search::Article without a class_name

