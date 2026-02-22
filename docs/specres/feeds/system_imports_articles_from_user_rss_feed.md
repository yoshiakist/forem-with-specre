---
id: "01KJ24EF4VQYFPB3R53Q4J2CJ1"
name: "system_imports_articles_from_user_rss_feed"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/feeds/import.rb`
- `app/services/feeds/assemble_article_markdown.rb`
- `app/services/feeds/check_item_medium_reply.rb`
- `app/services/feeds/check_item_previously_imported.rb`
- `app/services/feeds/clean_html.rb`
- `app/services/feeds/validate_url.rb`
- `app/sanitizers/feed_markdown_scrubber.rb`
- `app/workers/feeds/import_articles_worker.rb`
- `spec/services/feeds/import_spec.rb` (Test)
- `spec/services/feeds/assemble_article_markdown_spec.rb` (Test)
- `spec/services/feeds/clean_html_spec.rb` (Test)
- `spec/services/feeds/validate_url_spec.rb` (Test)
- `spec/sanitizers/feed_markdown_scrubber_spec.rb` (Test)
- `spec/workers/feeds/import_articles_worker_spec.rb` (Test)

## Functional Overview

The system periodically imports articles from each user's configured RSS/Atom feed URL. A Sidekiq worker (`ImportArticlesWorker`) fans out per-user import jobs in batches, then `Feeds::Import` orchestrates the full pipeline: filtering eligible users (active within 3 months, authorized to create articles, having a feed URL), fetching raw feed XML in parallel via HTTParty, parsing the XML in parallel via Feedjira, and then sequentially creating `Article` records for each new feed entry. Each feed item is checked to skip Medium reply items (`Feeds::CheckItemMediumReply`) and previously imported articles (`Feeds::CheckItemPreviouslyImported`). The item's HTML content is sanitized by `Feeds::CleanHtml`, transformed with platform-specific rules (Medium embeds, YouTube iframes, tweet blockquotes, relative image paths) by `Feeds::AssembleArticleMarkdown`, converted to Markdown, and assembled into a front-matter body. After each successful import, the article author is subscribed to all comments via `NotificationSubscription`, and a Slack notification is sent. Users' `feed_fetched_at` timestamp is updated after each batch.

## Design Intent

Feed fetching and parsing are parallelized (8 fetcher threads, 4 parser threads) while article creation is intentionally sequential to avoid database locking conflicts between concurrent writes. The `earlier_than` filter prevents re-fetching users whose feeds were recently processed, supporting both scheduled (4-hour cadence) and forced per-user imports. Article uniqueness is scoped per user (not globally), so the same source article can be imported by multiple users independently.

## Key Members

- `earlier_than` — optional time boundary; only users whose `feed_fetched_at` is before this value (or null) are processed
- `users_batch_size` — 50 users per batch
- `num_fetchers` — 8 parallel HTTP fetch threads
- `num_parsers` — 4 parallel Feedjira parse threads

## Scenarios

### Scheduled batch import for all eligible users

1. `ImportArticlesWorker` is invoked with no arguments (e.g., via sidekiq-cron).
2. The worker scopes to all users who have a feed URL and have been active within the past 3 months, defaulting `earlier_than` to 4 hours ago.
3. Users are batched and per-batch `ForUser` jobs are enqueued via `perform_bulk`.
4. Each `ForUser` job calls `Feeds::Import.call` with the scoped user IDs and the `earlier_than` cutoff.
5. `Feeds::Import` further filters out users whose `feed_fetched_at` is more recent than `earlier_than`, fetches and parses feeds in parallel, creates new articles, and records `feed_fetched_at` for the batch.

### Forced import for specific users

1. `ImportArticlesWorker` is called with an explicit list of user IDs.
2. The worker scopes to only those users and sets `earlier_than` to nil, bypassing the recency cutoff.
3. `Feeds::Import` processes all matching users regardless of their last fetch time.

### Feed item skipped as Medium reply

1. For each feed entry, `Feeds::CheckItemMediumReply` checks whether the item's host is `medium.com`, the item has no categories, and the content contains the title text.
2. If all three conditions are true, the item is identified as a comment reply and skipped without creating an article.

### Feed item skipped as previously imported

1. `Feeds::CheckItemPreviouslyImported` queries the user's existing articles for a matching title or `feed_source_url`.
2. If a match exists, the item is skipped to prevent duplicate articles for the same user.

### New article created from feed item

1. For a qualifying feed entry, the source URL is normalized (query string after `?source=` is stripped).
2. `Feeds::AssembleArticleMarkdown` builds a Markdown body: a front-matter header with title (truncated to 128 characters), publication date, up to 4 tags derived from feed categories, and an optional canonical URL if `feed_mark_canonical` is enabled.
3. The item's HTML content is cleaned by `Feeds::CleanHtml` (removes Medium tracking pixels, catchphrase paragraphs, and CSS classes; renames `figure` to `p`), then transformed for platform-specific embeds and relative image paths, and finally converted to GitHub-flavored Markdown.
4. An `Article` record is created with `published_from_feed: true` and `published: false`.
5. The author is subscribed to all comments on the new article via `NotificationSubscription`.

## Failures / Exceptions

- HTTP fetch errors for a single user are logged and skipped; the remaining users in the batch continue processing.
- Feedjira parse errors for a single user are logged and skipped.
- `Article.create!` or `NotificationSubscription.create!` failures for a single feed item are logged and skipped; subsequent items in the same feed continue.
- `Feeds::ValidateUrl` returns `false` for blank URLs or URLs that cannot be parsed by Feedjira, returning `true` only for valid feed URLs.
