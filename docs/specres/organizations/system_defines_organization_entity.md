---
id: "01KHYA9GWPEHZ06WJWDG1QKSK8"
name: "system_defines_organization_entity"
status: "draft"
---

## Related Files

- `app/models/organization.rb`
- `app/models/concerns/algolia_searchable/searchable_organization.rb`
- `spec/models/organization_spec.rb` (Test)

## Functional Overview

The `Organization` model represents a team or company account on the platform. It stores profile details (name, slug, summary, profile image, social usernames, CTA fields), display settings (background and text color hex values), and operational metadata (credits count, baseline score, fully-trusted flag, secret token). The model enforces comprehensive field-level validations (length limits, format constraints for hex colors and URLs, presence requirements for name and profile image), guarantees slug uniqueness across both `Organization` and `User` models via `UniqueAcrossModels`, and manages its own lifecycle through callbacks that handle slug history tracking, secret generation, CTA markdown evaluation, social-image regeneration, article propagation on attribute changes, and cache busting.

Algolia search indexing is provided by the `SearchableOrganization` concern, which indexes `name`, `tag_line`, `summary`, `slug`, and a computed `profile_image` URL. The search score is derived from the sum of published article scores, with timestamp-based replicas for ascending and descending sort.

## Key Members

- `Organization#slug` — URL-safe identifier, unique across users and organizations, downcased before validation; old slugs are preserved in `old_slug` and `old_old_slug` for redirect support
- `Organization#secret` — 100-character hex token auto-generated before first save; used for API authentication of organization-scoped requests
- `Organization#fully_trusted?` — boolean flag that exempts the organization from invitation rate limits
- `Organization#baseline_score` — non-negative integer used by the ranking system; admin-adjustable
- `Organization#destroyable?` — returns `true` only when the organization has exactly one membership, zero articles, and zero credits
- `Organization#enough_credits?(n)` — checks whether the organization has at least `n` unspent credits
- `Organization#check_for_slug_change` — on slug change, preserves old slugs and enqueues a worker to update article paths
- `Organization#conditionally_update_articles` — after update, re-saves articles when cached attributes (name, slug, profile image) change
- `AlgoliaSearchable::SearchableOrganization` — configures Algolia indexing with name, tag_line, summary, slug, profile_image, computed score, and timestamp replicas

## Scenarios

### Organization record is created with valid attributes

1. A caller creates a new `Organization` with a unique slug, valid name, and a profile image.
2. Before validation, the slug is downcased and the CTA body markdown (if present) is evaluated to processed HTML.
3. Before save, `@` characters are stripped from `twitter_username` and `github_username`, and a 100-character random hex secret is generated.
4. The record passes all validations: name present, slug length 2-30 and unique across models, hex colors match `/\A#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})\z/`, URLs are valid and non-local, numeric fields are in range.
5. After save, cache busting is enqueued and, if published articles exist, social image generation is enqueued.
6. The Algolia search index is updated asynchronously via `SearchIndexWorker`.

### Organization slug is changed

1. A caller updates the `slug` attribute of an existing organization.
2. `check_for_slug_change` fires before validation, shifting the current `old_slug` to `old_old_slug` and storing the previous slug value in `old_slug`.
3. `UpdateOrganizationArticlesPathsWorker` is enqueued to rewrite article paths from the old slug to the new one.
4. After the update commits, `conditionally_update_articles` detects the slug change and enqueues `SaveArticleWorker` for each article to update cached organization data.

### Organization cached attributes change

1. A caller updates an attribute listed in `Article::ATTRIBUTES_CACHED_FOR_RELATED_ENTITY` (such as `name`, `slug`, or `profile_image`).
2. After the update commits, `conditionally_update_articles` detects the change and enqueues `SaveArticleWorker` for each of the organization's articles.

### Organization is destroyed

1. A caller destroys an organization record (only possible when `destroyable?` returns `true`).
2. Dependent associations are handled: articles are nullified, credits restrict deletion, billboards and listings are destroyed, memberships and notifications are deleted.
3. After the destroy commits, cache busting is enqueued for the organization's path.

## Failures / Exceptions

- If `slug` is already taken by another Organization or User, the `unique_across_models` validation fails and the record is not saved.
- If `name` or `profile_image` is blank, presence validation fails.
- If `baseline_score` is negative, the numericality validation rejects it.
- If an organization has articles or credits, `destroyable?` returns `false` and the application layer prevents deletion.
