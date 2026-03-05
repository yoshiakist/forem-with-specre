---
id: "01KHZ28VAWY5TJ6GJYXZBVE4JN"
name: "user_can_search_reading_list"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/search_controller.rb`
- `app/services/search/reading_list.rb`
- `app/serializers/search/reading_list_article_serializer.rb`
- `app/javascript/searchableItemList/searchableItemList.js`
- `spec/services/search/reading_list_spec.rb` (Test)
- `spec/serializers/search/reading_list_article_serializer_spec.rb` (Test)

## Functional Overview

Authenticated users can search and filter their personal reading list (bookmarked articles). The reading list is accessed via the `/readinglist` page and queries the `/search/reactions` endpoint. Users can filter by bookmark status (confirmed, valid, archived), by tags, and by a free-text search term that matches against article body, title, tags, organization name, and author information. The frontend provides tag-based filtering with URL persistence and infinite-scroll pagination. A performance-optimized subquery approach avoids JOIN-based pagination slowdowns.

## Design Intent

The reading list query uses a subquery on the `reactions` table instead of a JOIN to avoid O(n) pagination slowdown that occurs when paginating over large joined result sets. User data is loaded in a separate query rather than through ActiveRecord includes, further reducing query complexity.

## Scenarios

### User searches reading list by keyword

1. User types a query into the reading list search box
2. Frontend sends a request to `/search/reactions` with the search term
3. `SearchController#reactions` delegates to `Search::ReadingList.search_documents` with the current user and term
4. Service applies full-text search via `.search_articles(term)` against article body, title, tags, organization name, and user information
5. Results are serialized with article title, path, reading time, tags, and author details

### User filters reading list by status

1. User selects a status filter (e.g., archived)
2. Service filters reactions by the specified status (confirmed, valid, or archived)
3. By default, only confirmed and valid reactions are included

### User filters reading list by tags

1. User clicks a tag in the reading list sidebar
2. Frontend updates the URL with the selected tag and queries `/search/reactions` with the tag parameter
3. Service filters articles whose `cached_tag_list` includes ALL requested tags (AND logic)
4. User can clear tag filters to return to the unfiltered list

### Reading list respects subforem boundaries

1. User views their reading list within a specific subforem
2. If the current subforem is not the root, service filters articles belonging to that subforem
3. If the current subforem is the root, articles from all subforems are included

### System returns total count for pagination

1. A reading list search is executed
2. Service returns both the serialized items and a `total` count representing all matching articles before pagination
3. Frontend uses this total to determine whether to show "load more" pagination
