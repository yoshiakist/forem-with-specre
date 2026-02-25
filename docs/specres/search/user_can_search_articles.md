---
id: "01KHZ22E63WBQWYFZNQVEA2EEE"
name: "user_can_search_articles"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/search_controller.rb`
- `app/controllers/stories/articles_search_controller.rb`
- `app/services/search/article.rb`
- `app/errors/search.rb`
- `app/javascript/Search/Search.jsx`
- `app/javascript/Search/SearchForm.jsx`
- `app/javascript/Search/SearchFormSync.jsx`
- `app/javascript/Search/index.js`
- `app/javascript/packs/Search.jsx`
- `app/javascript/packs/searchParams.js`
- `app/javascript/utilities/search/index.js`
- `app/javascript/articles/components/SearchSnippet.jsx`
- `app/views/stories/articles_search/index.html.erb` (Template)
- `app/views/stories/articles_search/_meta.html.erb` (Template)
- `app/views/stories/articles_search/_nav_menu.html.erb` (Template)
- `spec/services/search/article_spec.rb` (Test)
- `spec/requests/search_spec.rb` (Test)
- `spec/requests/search/feed_content_simple_spec.rb` (Test)
- `spec/requests/stories/articles_search_spec.rb` (Test)
- `spec/system/search/display_articles_search_spec.rb` (Test)
- `spec/system/search/search_title_spec.rb` (Test)
- `app/javascript/Search/__tests__/Search.test.jsx` (Test)
- `app/javascript/Search/__tests__/SearchFormSync.test.jsx` (Test)
- `app/javascript/utilities/__tests__/search.test.js` (Test)
- `app/javascript/Search/__stories__/SearchForm.stories.jsx`

## Functional Overview

Users can search for articles across the platform using a unified search page. The search is accessible from the header search box on any page and via the dedicated search results page at `/search`. The experience supports full-text search powered by PostgreSQL (with optional Algolia integration for real-time typeahead suggestions), sorting by relevance, newest, or oldest, and filtering by content type. The search page dynamically renders results with article metadata including title, reading time, tags, reaction counts, and comment counts. Keyboard shortcuts (pressing `/` focuses the search box) and URL synchronization ensure a seamless experience across navigation and viewport changes.

## Design Intent

The search architecture uses a dual approach: Algolia handles real-time typeahead suggestions in the search form for instant feedback, while PostgreSQL full-text search (`tsvector`) powers the main results for reliability and independence from third-party services. When Algolia is not configured, the system gracefully falls back to the PostgreSQL-only path. The frontend uses InstantClick for preloading search result pages to achieve near-instant navigation.

## Scenarios

### User searches articles by keyword

1. User types a query into the search box in the site header
2. System navigates to `/search?q=<query>&filters=class_name:Article`
3. `SearchController#feed_content` delegates to `Search::Article.search_documents` with the query term
4. Service applies PostgreSQL full-text search via `.search_articles(term)` against article body, title, tags, user name, and organization name
5. Results are ranked by relevance (title matches > tag matches > body matches) by default
6. User sees matching articles with title, reading time, tags, reactions count, and comments count

### User sorts article results

1. User clicks a sort tab (Relevance, Newest, or Oldest) on the search results page
2. System updates the URL with `sort_by` and `sort_direction` parameters
3. When sorted by newest/oldest, the service orders by `published_at` descending or ascending
4. When sorted by relevance (default with a search term), PostgreSQL `tsvector` document ranking is used
5. Without a search term and no explicit sort, articles are ordered by `hotness_score` descending, then `comments_count` descending

### System excludes unpublished articles

1. A search query is executed
2. The article search service builds its base relation via `Homepage::ArticlesQuery`, which only includes published articles
3. Unpublished or draft articles never appear in search results

### Search page displays proper metadata

1. User navigates to the search results page
2. The page title includes the search term (e.g., "Search Results - ruby") when a query is present
3. The page title shows a default community-branded title when no query is provided
4. OpenGraph and Twitter Card meta tags are set for social sharing

### Search form provides Algolia typeahead suggestions

1. User focuses the search box and begins typing
2. If Algolia API credentials are configured, the `SearchForm` component queries the Algolia index after a 200ms debounce
3. Matching suggestions appear in a dropdown below the search box
4. User can navigate suggestions with arrow keys and select with Enter
5. If Algolia is not configured, no suggestions are shown and the user submits the form normally
