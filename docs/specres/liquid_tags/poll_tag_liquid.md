---
id: "01KHY7Q18QQ15B7XBT5YDRTEQ6"
name: "poll_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/liquid_tags/poll_tag.rb`
- `app/views/liquids/_poll.html.erb` (Template)
- `app/assets/stylesheets/ltags/PollTag.scss`
- `spec/liquid_tags/poll_tag_spec.rb` (Test)

## Functional Overview

This specification defines the expected behavior of `PollTag` within the liquid_tags domain. The poll liquid tag allows article authors to embed interactive polls into their content. The tag parses a poll identifier from the liquid tag syntax, renders the poll UI via a partial template, and applies dedicated styles.


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- eq any admin?

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

