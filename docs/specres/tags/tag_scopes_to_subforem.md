---
id: "01KHYCE88A8Z44K257V7Q16KPK"
name: "tag_scopes_to_subforem"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/tag_subforem_relationship.rb
- spec/models/tag_subforem_relationship_spec.rb (Test)

## Functional Overview

`TagSubforemRelationship` is a join model that establishes a many-to-many relationship between tags and subforems. It controls which tags are available within specific subforems, enforcing uniqueness to prevent duplicate assignments.

## Scenarios

### System enforces unique tag-subforem pairs

1. A `TagSubforemRelationship` requires both a `tag_id` and a `subforem_id`.
2. The combination of `tag_id` and `subforem_id` must be unique; duplicate pairs are rejected.
3. The relationship is destroyed when its parent tag is deleted (via `dependent: :destroy` on the Tag side).
