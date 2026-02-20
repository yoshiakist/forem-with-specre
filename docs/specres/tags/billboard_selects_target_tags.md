---
id: "01KHYCRNMG4MM7NP4BV78E5WQ2"
name: "billboard_selects_target_tags"
status: "draft"
---

## Related Files

- app/javascript/billboard/tags.jsx

## Functional Overview

The `Tags` Preact component provides a multi-select autocomplete field for billboard (advertisement) administration. It allows admins to select up to 10 tags to target a billboard to specific content topics. The component fetches top tags on mount for static suggestions and supports dynamic search-as-you-type suggestions.

## Scenarios

### Admin selects target tags for a billboard

1. On mount, the component fetches suggested tags from `/tags/suggest` and displays them as static "Top tags" suggestions.
2. The admin can type to search for tags dynamically via the `fetchSuggestions` callback.
3. Up to 10 tags can be selected; additional selections are blocked by the `maxSelections` limit.
4. Existing tag selections (from `defaultValue`, a comma-separated string) are pre-populated on render.
5. Each selection change is synced back to the parent form via the `onInput` callback.
6. The admin can also define custom tag selections not present in suggestions (`allowUserDefinedSelections`).
