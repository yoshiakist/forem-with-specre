---
id: "01KJBV4Y67GJZ6K5AA2YX7YSZA"
name: "system_suggests_sidebar_articles_on_article_page"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/articles/get_user_stickies.rb`
- `app/services/articles/suggest_stickies.rb`
- `app/views/articles/_sticky_nav.html.erb`
- `spec/services/articles/get_user_stickies_spec.rb` (Test)
- `spec/services/articles/suggest_stickies_spec.rb` (Test)

## Functional Overview

When a reader views an article page, the sidebar displays a curated list of related articles below the author's profile card. The system first tries to surface up to 3 published articles from the same author (or organization) that share at least one tag with the current article, ordered by most recent publication. If no such articles exist, the sidebar falls back to a globally suggested set assembled from two pools: up to 3 articles that share tags with the current article and meet engagement thresholds, and up to 7 articles tagged with well-known discovery tags (career, productivity, discuss, explainlikeimfive) published within the last 5 days. The fallback set excludes articles by the same author and is randomly sampled down to the configured size. Both paths select only the minimal set of database columns required to render the sidebar, and the result is cached per article for 48 hours.

## Design Intent

The two-tier approach (author-first, then global suggestions) prioritizes keeping readers engaged with the same author's content before branching out to platform-wide discovery content. The column projection to only the fields needed by `_sticky_nav` avoids loading large columns like `body_markdown` and `processed_html`, keeping the sidebar query lightweight. The `discuss` tag is excluded from tag-matching to prevent generic discussion threads from dominating related-content results.

## Key Members

- `SUGGESTION_TAGS` — fixed list of discovery tags used for fallback suggestions: `career`, `productivity`, `discuss`, `explainlikeimfive`
- `DEFAULT_TAG_ARTICLES_LIMIT` (3) — maximum articles drawn from tag overlap in the fallback pool
- `DEFAULT_MORE_ARTICLES_LIMIT` (7) — maximum articles drawn from discovery tags in the fallback pool
- `sample_size` (default 3) — final number of suggested articles returned from the fallback path
- Engagement thresholds (`reaction_count_num`, `comment_count_num`) — relaxed to -1 / -2 outside production so tests always find candidates

## Scenarios

### Author has published related articles (user stickies path)

1. The sidebar partial determines the actor as the article's organization, or the article's author if no organization is set.
2. The system queries published articles by that actor that share at least one tag with the current article (excluding the "discuss" tag from matching), scoped to the current subforem.
3. The current article is excluded from the result set.
4. Up to 3 articles are returned, ordered newest-first.
5. The sidebar renders a "More from [author]" section listing each article's title and tags as links.

### Author has no related published articles (suggest stickies fallback)

1. The user stickies query returns no results.
2. The system assembles a fallback pool by combining:
   - Up to 3 published articles that share the current article's tags and meet engagement thresholds, published within the last 5 days.
   - Up to 7 published articles tagged with the discovery tags and meeting comment thresholds, published within the last 5 days.
3. Articles authored by the same user as the current article are excluded from the pool.
4. The current article itself is excluded from the pool.
5. The pool is randomly sampled down to the configured `sample_size` (default 3).
6. The sidebar renders a "Trending on [community]" section, showing each article's author avatar, title, and tags as links.

### Neither path returns articles

1. Both the user stickies query and the suggest stickies call return empty results.
2. The sidebar renders no article list section — only the author profile card and the billboard slot remain visible.

### Sidebar result is cached

1. On the first page view, the system runs the user stickies (and optionally the suggest stickies) query and caches the rendered HTML fragment keyed by the article ID and the actor's latest article update timestamp.
2. On subsequent views within 48 hours, the cached fragment is served without re-querying the database.
3. When the actor publishes or updates an article, the cache key changes (via `latest_article_updated_at`), causing fresh results to be rendered on the next request.

### Article has a nil or empty tag list

1. The current article's `cached_tag_list` is nil or blank.
2. `GetUserStickies` treats the tag list as empty (after splitting nil to an empty string); tag matching finds no overlap and returns an empty relation.
3. `SuggestStickies` similarly treats the tag pool as empty for the tag-article sub-query; the fallback still returns discovery-tag articles if they exist.
4. No error is raised; both services degrade gracefully to returning empty or discovery-only results.
