---
id: "01KHYA9GWPEHZ06WJWDG1QKSK8"
name: "organization_validates_and_manages_profile"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/organization.rb
- app/models/concerns/algolia_searchable/searchable_organization.rb
- spec/models/organization_spec.rb (Test)

## Functional Overview

The Organization model defines the core entity for community organizations, managing profile data validation, slug uniqueness across models (User, Podcast, Page), association lifecycle for articles/memberships/credits, cache invalidation on save, social image regeneration on profile changes, Algolia search indexing, and article path updates on slug changes.

## Scenarios

### Organization validates profile fields on save

1. The system requires name and profile_image to be present.
2. The system enforces length limits on all text fields (name ≤ 50, summary ≤ 250, tag_line ≤ 60, story/tech_stack ≤ 640, etc.).
3. The system validates bg_color_hex and text_color_hex against a hex color regex, allowing blank values.
4. The system validates company_size contains only digits (integer format).
5. The system validates url and cta_button_url as proper URLs with no local addresses.
6. The system validates baseline_score as a non-negative integer.

### Organization enforces slug uniqueness across models

1. The system downcases the slug before validation.
2. The system validates slug length between 2 and 30 characters, rejecting spaces and special characters.
3. The system rejects slugs already taken by a User, Podcast, or Page via `unique_across_models`.
4. The system rejects reserved slugs (e.g., "settings", "sitemap-*").

### Organization tracks slug history on change

1. When the slug changes, the system stores the previous slug in `old_slug` and the one before that in `old_old_slug`.
2. The system enqueues `Organizations::UpdateOrganizationArticlesPathsWorker` to update all article paths with the new slug.

### Organization generates a secret before save

1. If the secret is blank or nil, the system generates a 100-character random hex secret.
2. The system validates the secret is exactly 100 characters and unique.

### Organization triggers cache and social image updates after save

1. After save, the system enqueues `Organizations::BustCacheWorker` with the organization id and slug.
2. After save, if name or profile_image changed and the organization has published articles, the system enqueues `Images::SocialImageWorker`.
3. After update commit, if any cached entity attribute changed, the system bulk-enqueues `Organizations::SaveArticleWorker` for all associated articles.

### Organization indexes for Algolia search

1. The `SearchableOrganization` concern configures Algolia indexing with attributes: name, tag_line, summary, slug, profile_image, and a computed score from published articles.
2. The concern creates timestamp-based replicas for ascending and descending sort.
3. Index changes are processed asynchronously via `AlgoliaSearch::SearchIndexWorker`.

### Organization checks credit balance and destroyability

1. `enough_credits?` returns true when unspent credits count meets or exceeds the requested amount.
2. `destroyable?` returns true only when there is exactly one membership, zero articles, and zero credits.

## Key Members

- `slug` / `username`: URL-safe identifier, unique across User, Podcast, Page.
- `old_slug`, `old_old_slug`: Previous slug values for redirect support.
- `secret`: 100-char random hex token for organization verification.
- `fully_trusted`: Boolean flag that bypasses invitation rate limits.
- `baseline_score`: Non-negative integer used for article scoring adjustments.
