---
id: "01KHZ24CTQNRDZ5CAMD3TTT1KN"
name: "user_can_search_comments"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/search_controller.rb`
- `app/services/search/comment.rb`
- `app/serializers/search/comment_serializer.rb`
- `app/serializers/search/nested_user_serializer.rb`
- `spec/services/search/comment_spec.rb` (Test)
- `spec/serializers/search/comment_serializer_spec.rb` (Test)
- `spec/serializers/search/nested_user_serializer_spec.rb` (Test)
- `spec/system/search/display_comments_search_spec.rb` (Test)

## Functional Overview

Users can search for comments across the platform by selecting the "Comments" filter on the search results page. The comment search uses PostgreSQL full-text search against comment body text, with highlighted excerpts showing where the search term matched. Results include the comment's score, reaction counts, the commentable article's title, and the commenter's profile information. Only comments on published articles are included, and deleted or author-hidden comments are excluded.

## Scenarios

### User searches comments by keyword

1. User enters a search query and selects the "Comments" content type filter
2. `SearchController#feed_content` delegates to `Search::Comment.search_documents` with the query term
3. Service queries non-deleted comments on published articles, applying full-text search via `.search_comments(term)`
4. Results include highlighted excerpts with `<mark>` tags around matching text via PgSearch highlighting
5. Results are ordered by comment score (hotness) descending by default

### User sorts comment results by date

1. User selects a sort option (Newest or Oldest) while viewing comment results
2. Service applies `published_at` ordering in the requested direction (ascending or descending)
3. When no explicit sort is provided, results default to score-based ordering

### System excludes comments on unpublished articles

1. A comment search query is executed
2. The service joins the articles table and requires `articles.published = true`
3. Comments belonging to unpublished or draft articles are never returned

### System sanitizes highlight markup

1. Search results include PgSearch highlight fragments with `<mark>` tags
2. The system ensures that only safe `<mark>` tags appear in highlights
3. Any other HTML in the comment body is escaped to prevent XSS attacks
