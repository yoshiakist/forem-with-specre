---
id: "01KJBV1G647P4BRNVEY8SP0R1Q"
name: "system_suggests_related_articles_below_article"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/articles/suggest.rb`
- `app/views/articles/show.html.erb`
- `app/views/bottom_items/index.html.erb`
- `app/views/articles/_bottom_content.html.erb`
- `spec/services/articles/suggest_spec.rb` (Test)

## Functional Overview

When a reader views an article, the system displays up to four related articles in a "Read Next" section below the article body. The `Articles::Suggest` service selects candidates by first searching for published articles sharing at least one tag with the current article, ordered by hotness score and offset by a random amount to vary results. If tag-matched results do not fill the requested count, the service supplements them with other recently published, high-scoring articles from the same subforem authored by a different user. The result is cached per-article to avoid redundant queries, and the view renders author avatar, title, author name, and publication date for each suggestion.

## Design Intent

The two-phase selection strategy (tag-matched first, then fallback to general pool) ensures that closely related content is preferred while still filling the widget when an article has few or no tag matches. The random offset introduces variety across page loads so returning readers see different suggestions. Community size (total published article count) determines the quality thresholds applied: large communities use organic page-view counts as a quality signal, while small ones rely on a basic score floor.

## Key Members

- `MAX_DEFAULT: 4` — default number of suggestions returned unless overridden by the caller
- `max` — maximum number of suggestions to return; passed from the view as `4`
- `total_articles_count` — estimated count of all published articles in the subforem, used to branch quality thresholds and compute the random offset ceiling

## Scenarios

### Tag-matched suggestions fill the requested count

1. The reader opens an article that has one or more tags.
2. The system queries published articles from the same subforem, published within the last three months, sharing at least one tag with the current article, excluding the current article's author, with sufficient quality score.
3. The query is ordered by hotness score and shifted by a random offset.
4. If the number of tag-matched results equals the requested maximum, those results are returned directly without any additional query.
5. The view renders up to four "Read Next" links below the article.

### Tag-matched suggestions are insufficient — fallback fills the remainder

1. The reader opens an article whose tags match fewer articles than the requested maximum.
2. The system first collects all available tag-matched suggestions.
3. The system then queries a supplemental pool of recently published, high-scoring articles from the same subforem, excluding the current article's author and all already-collected tag-matched articles, ordered by hotness score with a random offset.
4. The two sets are merged without duplicates to reach the requested count.
5. The view renders the combined list below the article.

### Article has no tags — general pool used exclusively

1. The reader opens an article with an empty tag list.
2. The system skips the tag-based query entirely.
3. The system queries the general pool of recent, high-scoring articles from the same subforem excluding the current article's author.
4. Up to four articles are returned and rendered in the "Read Next" section.

### Result is cached

1. The first request for a given article's suggestions triggers `Articles::Suggest.call` and renders the partial.
2. The rendered HTML fragment is cached keyed on the article ID and the latest article update timestamp of the author or organization, with a 96-hour expiry.
3. Subsequent requests within the cache window skip the service call and serve the cached fragment directly.

### No suggestions available

1. The system returns an empty collection (e.g., the subforem has no other qualifying articles).
2. The `_bottom_content` partial receives an empty array and renders nothing, leaving the section absent from the page.
