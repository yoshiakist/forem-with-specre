---
id: "01KJ6EPTF1F31WB6DRV0YHEZ0N"
name: "visitor_sees_targeted_billboard"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/billboards_controller.rb`
- `app/models/billboard.rb`
- `app/models/billboard_placement_area_config.rb`
- `app/views/billboards/show.html.erb` (Template)
- `app/views/shared/_billboard.html.erb` (Template)
- `app/views/shared/_billboard_header.html.erb` (Template)
- `spec/requests/billboards_spec.rb` (Test)
- `spec/models/billboard_spec.rb` (Test)
- `spec/models/billboard_placement_area_config_spec.rb` (Test)

## Functional Overview

When a visitor (signed-in or signed-out) requests a billboard for a given placement area, `BillboardsController#show` orchestrates the full targeting flow. If billboards are globally disabled via the `DISABLE_BILLBOARDS` config flag, the endpoint immediately returns empty. For signed-out visitors, CDN-friendly cache-control headers are set using a per-placement-area configurable expiry, and a `Vary` header is added for geolocation when that feature flag is active. Admins or the owner of a published billboard may preview an unapproved billboard by supplying `bb_test_placement_area` and `bb_test_id` params. Otherwise, the controller calls `Billboard.for_display`, which first checks `BillboardPlacementAreaConfig.should_fetch_billboard?` to enforce per-area delivery rates for signed-in and signed-out users independently. Eligible billboards are fetched through `FilteredAdsQuery` (a separate concern) and, if a paired-billboard preference is active, the best paired match is returned immediately. Otherwise, `select_billboard_by_weighted_strategy` picks one of five strategies — `random_selection`, `new_and_priority`, `new_only`, `weighted_performance`, or `evenly_distributed` — proportionally to per-area configurable weights. The `new_and_priority` strategy uses `weighted_random_selection`, a SQL CTE that computes running weight sums and optionally boosts weight tenfold for billboards that list the current article as preferred. For tag-targeted feed placements, the controller samples a random subset of the viewer's top followed tags (between 5 and 32) so that higher-ranked tags appear more often.

## Design Intent

Splitting delivery probability from selection strategy via `BillboardPlacementAreaConfig` allows operators to throttle billboard load independently per placement area and user state without code changes. The five-strategy weighted picker lets product teams shift traffic between "show new/unproven ads" and "amplify top performers" by adjusting database weights rather than deploying code. The SQL-CTE weighted random avoids loading all eligible billboards into Ruby memory and produces statistically correct weighted draws in a single query. Randomizing the user-tag slice from the top of the followed-tag list creates an implicit bias toward higher-interest tags while still introducing variety, which serves both relevance and exploration goals.

## Key Members

- `RANDOM_USER_TAG_RANGE_MIN / MAX` (5 / 32) — bounds on how many of the visitor's top followed tags are passed for tag targeting on feed placements
- `BillboardPlacementAreaConfig#signed_in_rate` / `signed_out_rate` — integer 0–100 percentage controlling whether a billboard fetch is attempted
- `BillboardPlacementAreaConfig#cache_expiry_seconds` — per-area CDN cache TTL; defaults to 180 seconds
- `BillboardPlacementAreaConfig#selection_weights` — JSON hash mapping strategy name to relative weight; defaults are `random_selection: 5`, `new_and_priority: 30`, `new_only: 5`, `weighted_performance: 60`, `evenly_distributed: 0`
- `Billboard#preferred_article_ids` — integer array; when non-empty and `article_id_adjusted_weight` feature flag is on, the billboard's weight is multiplied by 10 in `weighted_random_selection`

## Scenarios

### Billboards are globally disabled

1. A request arrives with any `placement_area` param.
2. The controller checks the `DISABLE_BILLBOARDS` application config.
3. Because the value is `"yes"`, the controller renders an empty plain-text response and halts.

### Signed-out visitor receives a cached, geolocated billboard

1. A signed-out visitor requests a billboard for a specific placement area.
2. The controller looks up the `BillboardPlacementAreaConfig` for that area and sets `Cache-Control`, `Surrogate-Control`, and `X-Accel-Expires` headers using the configured expiry (defaulting to 180 seconds).
3. If the geolocation feature flag is enabled, the controller also adds `Vary: X-Cacheable-Client-Geo` so CDN nodes vary cached responses by coarse geolocation.
4. `Billboard.for_display` is called; the delivery rate check passes; `FilteredAdsQuery` narrows billboards by geolocation and other criteria.
5. A billboard is selected and rendered without a layout. A surrogate key header is set so the CDN can later purge by billboard ID.

### Admin previews an unpublished billboard

1. A signed-in admin requests a billboard with both `bb_test_placement_area` matching the current placement area and a `bb_test_id` pointing to an unapproved billboard.
2. The controller recognises the admin flag and fetches that exact billboard by ID, bypassing `for_display` entirely.
3. The unapproved billboard is rendered as if it were live.

### Published billboard owner previews their own billboard

1. A signed-in non-admin user supplies `bb_test_placement_area` and `bb_test_id` params.
2. The controller checks whether that billboard ID is in the approved-and-published set; it is.
3. The specific billboard is returned and rendered, even though the viewer is not an admin.

### Visitor receives a contextually selected billboard through weighted strategy

1. A visitor (signed-in or signed-out) requests a billboard for a placement area.
2. `BillboardPlacementAreaConfig.should_fetch_billboard?` rolls a random number against the area's delivery rate; the roll passes.
3. `FilteredAdsQuery` returns a set of eligible billboards filtered by audience segment, tags, geolocation, role names, and other criteria.
4. `select_billboard_by_weighted_strategy` draws a strategy proportionally from the configured weights (e.g., 60% chance of `weighted_performance`).
5. The selected strategy executes: for `new_and_priority`, `weighted_random_selection` runs a SQL CTE that sorts by running weight sum and picks the first row past a random threshold; if the current article ID matches any billboard's `preferred_article_ids` and the feature flag is on, that billboard's weight is boosted 10x.
6. The winning billboard is assigned to `@billboard`, cached by content hash on the view layer, and rendered without layout.

## Failures / Exceptions

- If `should_fetch_billboard?` returns false (delivery rate check fails), `for_display` returns `nil` and the controller renders an empty body.
- If `FilteredAdsQuery` returns no eligible billboards, `select_billboard_by_weighted_strategy` returns `nil` and nothing is rendered.
- If all configured strategy weights sum to zero, the strategy picker falls back to `Array#sample` (pure random) rather than raising an error.
- If the `new_and_priority` weighted SQL query returns no result, it falls back to `billboards_for_display.sample`.
