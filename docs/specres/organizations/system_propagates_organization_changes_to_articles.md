---
id: "01KJ02R9930HM3ZZNY5GTQB0X4"
name: "system_propagates_organization_changes_to_articles"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/models/organization.rb`
- `app/workers/organizations/save_article_worker.rb`
- `app/workers/organizations/update_organization_articles_paths_worker.rb`
- `spec/workers/organizations/save_article_worker_spec.rb` (Test)
- `spec/workers/organizations/update_organization_articles_paths_worker_spec.rb` (Test)

## Functional Overview

When an organization's attributes change, the system asynchronously propagates those changes to all articles belonging to the organization. Two distinct propagation paths exist: (1) when any attribute cached by articles (name, profile image, slug, username) changes on the organization, all associated articles are re-saved in bulk via `Organizations::SaveArticleWorker` so their cached entity data stays consistent; (2) when the organization's slug specifically changes, `Organizations::UpdateOrganizationArticlesPathsWorker` updates every article's stored path to reflect the new slug, replacing the old slug segment in the path with the new one. Both workers run on the high-priority queue and are triggered by model callbacks on the `Organization` model.

## Design Intent

Article records cache organization attributes (name, profile image, slug, username) to avoid expensive joins on read-heavy paths. When an organization changes, those cached values become stale, so a background re-save is the mechanism used to trigger the caching layer to refresh. The slug change path is handled separately because it also requires updating the stored `path` string on each article record, not just the cached entity — slug is part of the article URL and must remain consistent.

## Key Members

- `Article::ATTRIBUTES_CACHED_FOR_RELATED_ENTITY` — the list of organization attributes (`name`, `profile_image`, `profile_image_url`, `slug`, `username`) whose changes trigger a bulk article re-save
- `Organizations::SaveArticleWorker#perform(article_id)` — re-saves a single article by ID, refreshing its cached organization data
- `Organizations::UpdateOrganizationArticlesPathsWorker#perform(organization_id, old_slug, new_slug)` — finds the organization by ID, then updates each of its articles' `path` by substituting `old_slug` with `new_slug`

## Scenarios

### Organization cached attribute changes (e.g. name or profile image)

1. An organization record is saved and the `after_update_commit` hook fires `conditionally_update_articles`.
2. The method checks whether any attribute listed in `Article::ATTRIBUTES_CACHED_FOR_RELATED_ENTITY` was changed in this save.
3. If at least one such attribute changed, the IDs of all articles belonging to the organization are collected.
4. `Organizations::SaveArticleWorker.perform_bulk` is called with those article IDs, enqueuing one high-priority job per article.
5. Each job calls `Article#save` on the given article, causing the article to re-cache the organization's current data.

### Organization slug changes

1. Before the organization record is validated, the `before_validation` hook `check_for_slug_change` runs.
2. If the slug value has changed, the old slug is recorded on the model (`old_slug`, `old_old_slug`) and `Organizations::UpdateOrganizationArticlesPathsWorker.perform_async` is enqueued with the organization ID, the previous slug, and the new slug.
3. The worker fetches the organization by ID. If the organization no longer exists, it exits early.
4. For each article belonging to the organization, the worker replaces the old slug segment in `article.path` with the new slug and persists the change.

### No cached attributes changed

1. An organization record is saved but none of the attributes in `Article::ATTRIBUTES_CACHED_FOR_RELATED_ENTITY` were modified.
2. `conditionally_update_articles` detects no matching changed attributes and returns without enqueuing any jobs.
3. Articles are not affected.

## Failures / Exceptions

- If the organization is deleted between the time the slug-change job is enqueued and when it executes, `Organization.find_by(id: organization_id)` returns `nil` and the worker exits without error, leaving article paths unchanged.
- `SaveArticleWorker` uses `Article.find`, which will raise `ActiveRecord::RecordNotFound` if the article was deleted before the job runs; Sidekiq's standard retry mechanism handles this.
