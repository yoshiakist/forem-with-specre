---
id: "01KHYCB979HE8GAWAK6V94BANV"
name: "tag_classifies_content"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/tag.rb
- app/lib/constants/tags.rb
- app/models/concerns/taggable.rb
- spec/models/tag_spec.rb (Test)

## Functional Overview

The `Tag` model (extending `ActsAsTaggableOn::Tag`) is the central entity for content classification in Forem. Tags can be arbitrary or supported, may have moderators who form sub-communities, and can be consolidated via aliasing. Each tag carries metadata including colors, categories, markdown-rendered rules, badge associations, and a computed hotness score. A frozen set of "flare" tag names in `Constants::Tags` designates special community-purpose tags.

## Scenarios

### Tag validates naming rules

1. A tag name must be present, at most 30 characters, and consist only of alphanumeric characters (including Unicode letters such as Arabic, Chinese, and Polish).
2. Names containing symbols (e.g. `#`, `+`, `™`, musical notes) or prohibited Unicode whitespace characters are rejected.
3. Tag names are stored in lowercase.

### Tag validates color format

1. Both `bg_color_hex` and `text_color_hex` must match the hex color pattern `#RRGGBB` or `#RGB` when present.
2. If a color value is provided without a leading `#`, the system prepends it automatically before validation.
3. Nil color values are permitted.

### Tag validates category and alias

1. Every tag must have a `category` from the allowed set: `uncategorized`, `language`, `library`, `tool`, `site_mechanic`, `location`, `subcommunity`.
2. When `alias_for` is set, the referenced tag name must exist in the database; otherwise validation fails.
3. Blank `alias_for` values are automatically nullified via `StringAttributeCleaner`.

### Tag processes markdown and sanitizes summary on save

1. Before validation, `rules_markdown` and `wiki_body_markdown` are converted to HTML.
2. Before validation, `short_summary` is stripped of all HTML tags.
3. The `updated_at` timestamp is explicitly set on every save (since the base class does not do this by default).

### Tag calculates hotness score

1. Before save, the system queries articles published in the last 7 days that are tagged with this tag's name.
2. The hotness score is computed as: `(SUM(comments_count) * 14 + SUM(score)) + (article_count * ((taggings_count + 6) / 2))`.
3. This score is used to rank tags by recent engagement.

### Tag resolves aliases

1. `Tag.aliased_name(word)` looks up a tag by name and returns the `alias_for` value if present, otherwise the tag's own name; returns nil if the tag does not exist.
2. `Tag.find_preferred_alias_for(word)` returns the preferred alias or the downcased input if no alias is found.
3. The `aliased` scope returns tags that have an `alias_for` value; the `direct` scope returns those without.

### Tag tracks user following with points

1. `Tag.followed_tags_for(follower:)` returns tags a user follows, including the follow `points` attribute, ordered by hotness score.
2. `Tag.followed_by(user, explicit_points)` returns tags followed by a user filtered by a points range, ordered by points descending.
3. `Tag.antifollowed_by(user)` returns tags the user has hidden (negative explicit points).
4. `Tag#points` defaults to 0 when no points attribute is present.

### Tag supports accessible naming

1. When the `favor_accessible_name_for_tag_label` feature flag is enabled, `accessible_name` returns `pretty_name` if present, otherwise falls back to `name`.
2. When the feature flag is disabled, `accessible_name` always returns `name`.

### Tag busts cache after commit

1. After commit, the system enqueues a `Tags::BustCacheWorker` job with the tag name.
2. The tag-colors server cache entry is also deleted.

### Tag updates suggested tags setting on change

1. When the `suggested` flag changes, the system updates the `Settings::General.suggested_tags` setting with the names of all suggested-for-onboarding tags.

## Key Members

- `ALLOWED_CATEGORIES` — frozen array of valid tag categories
- `FLARE_TAG_NAMES` (in `Constants::Tags`) — frozen array of 13 special community tag names (ama, discuss, help, showdev, etc.)
- `hotness_score` — computed popularity metric based on recent article engagement
- `alias_for` — name of the preferred tag when this tag is an alias
- `supported` — boolean flag indicating whether the tag is officially supported
- `suggested` — boolean flag for onboarding suggestions

## Design Intent

Tags extend `ActsAsTaggableOn::Tag` rather than `ApplicationRecord`, which means some standard Rails behaviors (like automatic `updated_at` tracking) must be manually implemented. The alias system allows tag consolidation without losing historical taggings. The hotness score provides a recency-weighted ranking metric for surfacing active topics.
