---
id: "01KHYCCYF91FZD91NRC64NCGPA"
name: "tag_adjustment_modifies_article_tags"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/tag_adjustment.rb
- spec/models/tag_adjustment_spec.rb (Test)

## Functional Overview

`TagAdjustment` manages requests to add or remove tags from articles. Each adjustment is permission-gated: only tag moderators (scoped to the specific tag) and elevated users (admins, super moderators) may create adjustments. The model enforces article tag limits and validates that removal targets actually exist on the article. Adjustments follow a status workflow and can generate notifications.

## Scenarios

### Privileged user creates a tag adjustment

1. A tag moderator may create a tag adjustment for tags they moderate.
2. Multiple tag moderators may each create adjustments for the same tag on the same article.
3. A tag moderator may not create an adjustment for a tag they do not moderate.
4. Admins and super moderators may create tag adjustments for any tag.
5. Regular users without tag moderator role or elevated privileges are rejected.

### System validates adjustment type and status

1. The `adjustment_type` must be either `removal` or `addition`; any other value is rejected.
2. The `status` must be one of `committed`, `pending`, `committed_and_resolvable`, or `resolved`; any other value is rejected.
3. The `tag_name` must be present.

### System enforces article tag limits

1. An addition adjustment is rejected if the article already has 4 tags (the maximum).
2. A removal adjustment is rejected if the specified tag name is not currently on the article's tag list.
3. Tag name comparison for removal is case-insensitive.

## Failures / Exceptions

- `user_id` error when the user lacks privilege to adjust the tag.
- `tag_id` error when attempting to remove a tag not present on the article.
- `base` error when attempting to add a tag to an article that already has 4 tags.
