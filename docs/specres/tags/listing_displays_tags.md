---
id: "01KHYCSHNS0S69CWGV0Q67HZVW"
name: "listing_displays_tags"
status: "draft"
---

## Related Files

- app/javascript/listings/dashboard/rowElements/tags.jsx

## Functional Overview

The `Tags` Preact component renders a list of clickable tag links within a listings dashboard row. Each tag links to a filtered listings view for that tag. It is a stateless presentational component.

## Scenarios

### Listing row displays its tags as filter links

1. The component receives a `tagList` array of tag name strings.
2. Each tag is rendered as an anchor link with href `/listings?t={tag}`, prefixed with `#`.
3. Links include the `data-no-instant` attribute to bypass Turbolinks/InstantClick prefetching.
4. Tags are displayed inline within a span element.
