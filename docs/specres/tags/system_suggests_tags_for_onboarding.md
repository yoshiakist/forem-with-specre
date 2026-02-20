---
id: "01KHYCPT4S16SQD5XX64HWHEJ2"
name: "system_suggests_tags_for_onboarding"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/queries/tags/suggested_for_onboarding.rb
- spec/queries/tags/suggested_for_onboarding_spec.rb (Test)

## Functional Overview

`Tags::SuggestedForOnboarding` is a query object that returns a curated list of tags for new user onboarding. It prioritizes tags explicitly marked as suggested, then fills remaining slots with supported tags, all ordered by hotness score. The result is capped at 45 tags.

## Scenarios

### System returns suggested tags for onboarding

1. The query first retrieves all tags where `suggested` is true, ordered by hotness score descending.
2. If the count of suggested tags meets or exceeds the maximum (45), only those tags are returned.
3. If fewer than 45 suggested tags exist, the query expands to include tags where `supported` is true, combining both sets with an OR condition.
4. The combined result is ordered by hotness score descending and limited to 45 tags.
5. Suggested tags always appear in the result set; supported tags fill any remaining capacity.

## Key Members

- `MAX` — the maximum number of tags to return (45)
