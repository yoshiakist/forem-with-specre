---
id: "01KHY7Q0R6S00GRWHN1FQV5GE6"
name: "search_search_title_system"
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
- spec/system/search/search_title_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Search` within the search domain.

### Behavioral Areas

- **Search page title**: includes the search term in title and heading
- **when search query param exists**: includes the search term in title and heading
- **when search query param doesn**: includes the search term in title and heading

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

### S-1: includes the search term in title and heading

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes the search term in title and heading

### S-2: /search?q=helloworld

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /search?q=helloworld

### S-3: does not include search term in title and heading

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not include search term in title and heading

### S-4: /search

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** /search

