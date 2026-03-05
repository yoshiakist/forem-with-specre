---
id: "01KJXW7E07AADE8M9MG7XVBZN8"
name: "system_displays_listings_in_article_sidebar"
status: "draft"
---

## Related Files

- `app/views/articles/_sidebar_listings.html.erb`
- `app/models/listing.rb`

## Functional Overview

When a visitor browses an article page without any timeframe filter applied, the sidebar partial queries all published listings and, if any exist, renders a secondary card widget showing up to five of the most recently bumped listings. Each listing entry links to its detail page and displays the listing title alongside its category. A "See all" link navigates to the full listings index, and a "Post a listing" link points to the new-listing form. If the timeframe filter is present or there are no published listings, the entire widget is suppressed.

## Design Intent

The sidebar fetches only the columns it needs (`title`, `classified_listing_category_id`, `slug`, `bumped_at`) to keep the query lightweight. Ordering by `bumped_at` descending and capping results at five ensures the widget stays concise while surfacing the most recently active listings.

## Key Members

- `@listings` — collection of published `Listing` records, selected with only the columns needed for display
- `bumped_at` — timestamp used to sort listings so the most recently promoted entries appear first
- `params[:timeframe]` — when present, suppresses the entire sidebar widget

## Scenarios

### Sidebar renders published listings

1. A visitor opens an article page with no timeframe query parameter.
2. The system queries all published listings, selecting only the display-relevant columns.
3. The sidebar card appears with up to five listings, ordered by most recently bumped first.
4. Each listing entry shows the listing title and its category, linked to the listing's own page.
5. A "See all" link to the listings index and a "Post a listing" link are shown at the bottom of the widget.

### Sidebar is hidden when timeframe filter is active

1. A visitor opens an article page with a non-blank `timeframe` query parameter (e.g., a filtered feed view).
2. The system skips the widget entirely regardless of whether published listings exist.
3. No sidebar card is rendered.

### Sidebar is hidden when no published listings exist

1. A visitor opens an article page with no timeframe filter.
2. The system queries published listings and finds none.
3. The sidebar widget is not rendered.
