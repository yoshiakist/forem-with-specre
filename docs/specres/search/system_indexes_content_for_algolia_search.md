---
id: "01KHZ2B1BF232HFDSKGKHDSF6F"
name: "system_indexes_content_for_algolia_search"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/models/concerns/algolia_searchable.rb`
- `app/models/concerns/algolia_searchable/searchable_article.rb`
- `app/models/concerns/algolia_searchable/searchable_comment.rb`
- `app/models/concerns/algolia_searchable/searchable_organization.rb`
- `app/models/concerns/algolia_searchable/searchable_podcast_episode.rb`
- `app/models/concerns/algolia_searchable/searchable_tag.rb`
- `app/models/concerns/algolia_searchable/searchable_user.rb`
- `app/workers/algolia_search/search_index_worker.rb`
- `spec/workers/algolia_search/search_index_worker_spec.rb` (Test)

## Functional Overview

The system asynchronously indexes platform content (articles, comments, podcast episodes, tags, and users) into Algolia search indices. Each model type includes the `AlgoliaSearchable` concern, which dynamically loads a type-specific searchable module defining which attributes to index, conditional indexing rules, and custom ranking criteria. When a model record is created or updated, a Sidekiq background worker (`AlgoliaSearch::SearchIndexWorker`) processes the index update asynchronously. Each content type maintains timestamp-based replica indices for alternative sort orders. The entire indexing pipeline can be globally enabled or disabled via `Settings::General.algolia_search_enabled?`.

## Design Intent

Indexing is decoupled from model persistence via Sidekiq workers to avoid blocking user-facing requests. Each content type defines its own conditional indexing logic to keep the Algolia index clean — low-quality content (negative-score articles, spam comments, bad-actor users) is automatically excluded. Per-environment indices prevent development/staging data from contaminating production search.

## Scenarios

### System indexes articles with quality filtering

1. An article is created or updated
2. The `SearchableArticle` concern checks `indexable`: the article must be published, have a positive score, and `published_at` must be in the past
3. If indexable, `trigger_sidekiq_worker` enqueues `AlgoliaSearch::SearchIndexWorker`
4. The worker calls `index!` on the record, sending title, tag list, first 1000 characters of body, user info, reading time, scores, and subforem ID to Algolia
5. Timestamp-based replica indices are maintained for ascending and descending date sorting

### System indexes comments with spam filtering

1. A comment is created or updated
2. The `SearchableComment` concern checks `bad_comment?`: comments with negative scores are excluded
3. Qualifying comments are indexed with commentable info, body, score, user details, and timestamps

### System indexes users with bad-actor filtering

1. A user profile is created or updated
2. The `SearchableUser` concern checks `bad_actor_or_empty_profile?`: users with negative scores, banished status, spam/suspended roles, or low activity (fewer than 4 articles AND comments, fewer than 4 badges) are excluded
3. Qualifying users are indexed with name, username, badge count, and profile image

### System processes index updates asynchronously

1. A model change triggers `trigger_sidekiq_worker`
2. `AlgoliaSearch::SearchIndexWorker` runs on the `medium_priority` queue with up to 5 retries
3. If `remove` flag is true, the worker deletes the record from the Algolia index
4. If `remove` flag is false, the worker calls `index!` to create or update the index entry
5. If Algolia search is globally disabled, the worker returns early without processing

### System respects global enable/disable setting

1. An administrator disables Algolia search via `Settings::General`
2. The `AlgoliaSearchable` concern sets `disable_indexing` based on the setting
3. The background worker checks the setting and skips processing when disabled
4. No index updates are sent to Algolia until the setting is re-enabled
