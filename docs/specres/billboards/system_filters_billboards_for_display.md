---
id: "01KJ6E7PRKSFS5KXNECTT1W0C3"
name: "system_filters_billboards_for_display"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/queries/billboards/filtered_ads_query.rb`
- `app/helpers/billboard_helper.rb`
- `spec/queries/billboards/filtered_ads_query_spec.rb` (Test)
- `spec/helpers/billboard_helper_spec.rb` (Test)

## Functional Overview

The system filters the pool of available billboards down to a display-eligible set by applying a sequence of progressive constraints. Starting from the full `Billboard` relation (or a pre-scoped subset), `Billboards::FilteredAdsQuery` removes ads that are unapproved, unpublished, outside the requested placement area, incompatible with the visitor's subforem, browser context, cookie consent state, article or user tag context, audience segment membership, role-based targeting, geographic location, ad type, and promotional-pause status. Signed-in users additionally receive role and survey-completion filtering. The surviving ads are ordered by descending `success_rate`. `BillboardHelper` provides supporting utilities including the `feed_targeted_tag_placement?` predicate (used to restrict untagged-ad fallback to home-feed placements only) and methods for assembling audience-segment option arrays used by the admin UI.

## Design Intent

Filters are applied in a deliberate sequence so that each step narrows the relation before the next one runs. The `type_of_ads` filter is intentionally placed near the end because it inspects whether any community-type ads exist after all prior filters have been applied — a position-sensitive check. The geographic-location filter is guarded by a feature flag to allow safe rollout. Survey-completion filtering has its own application-level kill switch (`SKIP_SURVEY_COMPLETION_FILTERING` env var) for emergency disabling without a deploy.

## Key Members

- `area` — placement area string (e.g., `"post_sidebar"`, `"feed_first"`) used to restrict ads to the correct slot
- `user_signed_in` — controls which authentication audience (`logged_in` / `logged_out` / `all`) is shown, and gates role and survey filters
- `article_tags` / `user_tags` — tag lists used to match tagged ads or fall back to untagged ads
- `permit_adjacent_sponsors` — when `false`, external-type ads are suppressed regardless of other criteria
- `location` — ISO 3166-2 string parsed into a `Geolocation`; used for country/region targeting when the feature flag is on
- `cookies_allowed` — when `false`, ads requiring cookies are excluded
- `subforem_id` — falls back to `RequestStore.store[:subforem_id]` if not explicitly supplied

## Scenarios

### Approved and published gate

1. A visitor requests ads for a placement area.
2. The system discards any billboard that is not both approved and published.
3. Only the remaining approved-and-published ads continue through subsequent filters.

### Placement-area, subforem, and browser-context narrowing

1. Ads are filtered to those whose `placement_area` matches the requested area.
2. Ads are filtered to those whose `include_subforem_ids` is empty or contains the current subforem ID (resolved from the parameter or `RequestStore`).
3. When a `user_agent` string is provided, ads are filtered to those whose `browser_context` is compatible (in-app mobile, mobile web, or desktop).

### Tag-based targeting on article pages and home feed

1. When an `article_id` is supplied and the article has tags, the system shows ads that match any article tag plus ads with no tags at all; ads tagged with non-matching topics are removed.
2. When an `article_id` is supplied but the article has no tags, only untagged ads are shown.
3. When `user_tags` are present (regardless of article context), the same tag-or-untagged logic is applied using the user's followed tags.
4. When the placement area is a home-feed slot and the user has no tags, only untagged ads are shown (this fallback is not applied to non-feed placements).

### Authentication audience and role filtering

1. Signed-in visitors receive ads targeted to `logged_in` or `all`; signed-out visitors receive ads targeted to `logged_out` or `all`.
2. For signed-in visitors, ads are further filtered by `target_role_names` and `exclude_role_names` against the user's current roles.

### Community versus in-house/external ad type selection

1. When an `organization_id` is provided and community-type ads exist for that organization after all prior filters, only those community ads are returned.
2. Otherwise, in-house ads are always included; external ads are included only if `permit_adjacent_sponsors` is `true`.

### Geographic location targeting

1. When the `billboard_location_targeting` feature flag is disabled, all ads pass through regardless of their `target_geolocations`.
2. When the flag is enabled and no visitor location is known, only ads with an empty `target_geolocations` list are shown.
3. When the flag is enabled and a visitor location (country or country-region) is known, ads whose `target_geolocations` is empty or includes the visitor's country or region are shown; others are excluded.

### Paused promotional organizations and survey-completion exclusion

1. Billboards belonging to organizations whose promotional impressions are currently paused (tracked via a cache key) are excluded; billboards with no organization or from active organizations pass through.
2. For signed-in users, billboards configured to exclude survey completions are hidden if the user has already completed any of the billboard's specified surveys, unless the `SKIP_SURVEY_COMPLETION_FILTERING` environment variable is set to `"yes"`.

## Failures / Exceptions

- `BillboardHelper#single_audience_segment_option` raises `ArgumentError` if called on a billboard that has no associated audience segment.
- If the paused-organization cache is empty or nil, the promotional-pause filter is skipped entirely and all billboards pass through.
- An unsupported `user_agent` string that matches none of the known patterns causes the browser-context filter to be skipped, allowing all browser-context variants through.
