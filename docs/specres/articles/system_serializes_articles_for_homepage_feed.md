---
id: "01KJXTGF4X3QMRYRP6R1F5828B"
name: "system_serializes_articles_for_homepage_feed"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/queries/homepage/articles_query.rb`
- `app/services/homepage/fetch_articles.rb`
- `app/serializers/homepage/article_serializer.rb`
- `spec/queries/homepage/articles_query_spec.rb` (Test)
- `spec/services/homepage/fetch_articles_spec.rb` (Test)
- `spec/serializers/homepage/article_serializer_spec.rb` (Test)

## Functional Overview

When the homepage feed (or profile, organization, or tag index pages) requests articles, the system executes a three-stage pipeline. `ArticlesQuery` builds a filtered, sorted, and paginated `ActiveRecord::Relation` scoped to published, non-negative-score articles from the current subforem, selecting only the columns the feed needs and applying optional filters for approval status, publication date, author, organization, included tags, and hidden tags. `FetchArticles` acts as the orchestrating entry point, forwarding all filter and pagination parameters to `ArticlesQuery` and passing the resulting relation to `ArticleSerializer`. `ArticleSerializer` batch-loads flare tag data in a single SQL query via `FetchTagFlares`, then eager-loads user and organization associations, and transforms each article record into a flat attribute hash containing scalar fields, a nested user hash, an optional nested organization hash, and a `flare_tag` entry. The final output is an array of plain hashes ready for JSON serialization.

## Design Intent

Tag flare data is fetched before the user/organization eager-load so that the `FetchTagFlares` query operates on a lighter relation without those joins. This avoids the N+1 pattern that the `FlareTag` class would otherwise produce per article.

The `ArticlesQuery` select list is kept minimal (only the columns the serializer needs) to reduce memory and bandwidth on what can be a large result set.

## Key Members

- `ArticlesQuery::ATTRIBUTES` — the fixed list of article columns selected in every query; keeps the result set lean.
- `ArticlesQuery::SORT_PARAMS` — allowlist of column names that may be used as sort keys; unknown sort keys are silently ignored.
- `ArticlesQuery::DEFAULT_PER_PAGE` / `MAX_PER_PAGE` — page size defaults to 60, capped at 100.
- `FetchArticles::DEFAULT_PER_PAGE` — mirrors the query default for the service layer interface.

## Scenarios

### Default feed retrieval

1. A caller invokes `FetchArticles.call` with no arguments.
2. `ArticlesQuery` scopes the relation to published, full-post articles from the current subforem with a score of zero or above, selects only the feed-relevant columns, and paginates to the first 60 results.
3. `ArticleSerializer` batch-fetches flare tags, eager-loads users and organizations, and returns an array of attribute hashes.

### Filtered feed by author, organization, or tags

1. A caller passes one or more of `user_id`, `organization_id`, `tags`, or `hidden_tags` to `FetchArticles.call`.
2. `ArticlesQuery` applies the corresponding `WHERE` clauses: filtering to the specified author or organization, restricting to articles carrying any of the included tags, and excluding articles carrying any of the hidden tags.
3. Only articles satisfying all active filters reach the serializer.

### Approval-filtered feed

1. A caller passes `approved: true` (or `false`) to `FetchArticles.call`.
2. `ArticlesQuery` adds a `WHERE approved = ?` clause; when `approved` is `nil` (the default), no approval filter is applied and both approved and unapproved articles are returned.

### Sorted feed

1. A caller passes `sort_by` and an optional `sort_direction` to `FetchArticles.call`.
2. `ArticlesQuery` validates that `sort_by` is one of `hotness_score`, `public_reactions_count`, or `published_at`; unrecognized keys are silently ignored and no `ORDER BY` clause is added.
3. When a valid sort key is supplied, results are ordered by that column in the requested direction (defaulting to descending).

### Paginated feed

1. A caller passes `page` and `per_page` to `FetchArticles.call`.
2. `ArticlesQuery` converts the zero-based `page` index to one-based, caps `per_page` at 100, and applies Kaminari-style `.page().per()` pagination.
3. The serializer processes only the records on the requested page.

### Serialized output shape

1. `ArticleSerializer.serialized_collection_from` receives a relation.
2. Each article is transformed into a hash with scalar fields (`id`, `title`, `path`, `reading_time`, `published_at_int`, `readable_publish_date`, `public_reactions_count`, `comments_count`, `tag_list`, `flare_tag`, `video_duration_string`, `cloudinary_video_url`, `class_name`, `user_id`, `public_reaction_categories`) plus a nested `user` hash (`name`, `profile_image_90`, `username`) and, when present, a nested `organization` hash (`name`, `profile_image_90`, `slug`).
3. For articles with `type_of == "status"`, the hash also includes `title_finalized_for_feed` and `title_for_metadata`.
