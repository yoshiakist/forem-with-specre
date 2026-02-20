---
id: "01KHYAKARS8WVZ96MGFRRX02R5"
name: "organization_updates_article_paths_on_slug_change"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/workers/organizations/update_organization_articles_paths_worker.rb
- app/workers/organizations/save_article_worker.rb
- spec/workers/organizations/update_organization_articles_paths_worker_spec.rb (Test)
- spec/workers/organizations/save_article_worker_spec.rb (Test)

## Functional Overview

When an organization's slug changes, two high-priority workers ensure article URLs remain correct: UpdateOrganizationArticlesPathsWorker replaces the old slug with the new slug in all article paths, and SaveArticleWorker re-saves individual articles to trigger model callbacks that update cached entities.

## Scenarios

### Worker updates article paths on slug change

1. The worker receives organization_id, old_slug, and new_slug.
2. The worker looks up the organization by ID; exits silently if not found.
3. The worker iterates over all organization articles and replaces occurrences of the old slug with the new slug in each article's path.

### Worker re-saves article to trigger callbacks

1. The SaveArticleWorker receives an article_id.
2. The worker finds the article and calls save, triggering any model callbacks (e.g., cached entity updates).
3. Both workers run on the high_priority queue.
