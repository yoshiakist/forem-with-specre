---
id: "01KJ6E7GAHP8M3SQND6QQNEDED"
name: "admin_can_configure_placement_area"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/admin/billboard_placement_area_configs_controller.rb`
- `app/models/billboard_placement_area_config.rb`
- `app/views/admin/billboard_placement_area_configs/index.html.erb` (Template)
- `app/views/admin/billboard_placement_area_configs/edit.html.erb` (Template)
- `spec/controllers/admin/billboard_placement_area_configs_controller_spec.rb` (Test)
- `spec/models/billboard_placement_area_config_spec.rb` (Test)

## Functional Overview

Admins can view and edit per-placement-area billboard delivery settings through a dedicated admin UI. Each placement area has its own configuration record storing the percentage of signed-in and signed-out users who will be shown billboards, a cache expiry duration, and relative weights for five billboard selection strategies (random, new-and-priority, new-only, weighted-performance, and evenly-distributed). When the index page loads, the system automatically creates default configuration records for any placement areas that do not yet have one. Saving a configuration busts the in-memory cache so changes take effect immediately.

## Design Intent

Separating delivery rates and selection weights into a per-placement-area database record allows operators to tune billboard behavior independently for each surface without a code deploy. The index-time auto-provisioning of missing records ensures there is always a config to edit, even for newly added placement areas. Relative weights (rather than percentages that must sum to 100) reduce the burden on operators when adjusting individual strategies.

## Key Members

- `signed_in_rate` / `signed_out_rate` — integer 0–100 controlling what percentage of users in each auth state receive a billboard for this placement area
- `cache_expiry_seconds` — optional integer 0–86400; when nil the system falls back to `DEFAULT_BILLBOARD_CACHE_EXPIRY_SECONDS` (180 s); 0 disables caching
- `selection_weights` — JSON hash keyed by strategy name (`random_selection`, `new_and_priority`, `new_only`, `weighted_performance`, `evenly_distributed`); missing keys are filled from `DEFAULT_SELECTION_WEIGHTS` at read time
- `CACHE_KEY` / `CACHE_EXPIRY` — shared cache key and 1-hour TTL used by `all_configs`

## Scenarios

### Admin views all placement area configurations

1. An admin navigates to the billboard placement area configs index page.
2. The system queries all existing configuration records, ordered alphabetically by placement area name.
3. For any placement areas defined in `Billboard::ALLOWED_PLACEMENT_AREAS` that lack a record, the system creates one with default delivery rates of 100% for both signed-in and signed-out users. If creation fails for a particular area it is logged as a warning and the page still renders.
4. The page displays a table listing each placement area with its current signed-in rate and signed-out rate, plus an edit link.

### Admin edits a placement area configuration

1. The admin clicks the edit link for a specific placement area.
2. The system loads the configuration record and resolves its human-readable area name.
3. The edit form displays fields for signed-in rate, signed-out rate, cache expiry, and five range-slider controls for selection strategy weights. Each slider shows its current value live as the admin drags it.
4. The admin adjusts one or more values and submits the form.
5. The system validates and persists the changes, then redirects to the index with a success flash message and busts the config cache.

### Update fails validation

1. The admin submits the edit form with an out-of-range value (e.g., signed-in rate > 100 or < 0).
2. The model validation rejects the record.
3. The controller re-renders the edit form and sets a danger flash message containing the full validation error text. No changes are saved.

### System sanitizes negative selection weights

1. The admin submits selection weight values that include negative integers (possible via direct POST manipulation).
2. The controller's `config_params` method clamps any negative weight to 0 before passing them to the model.
3. The record is saved with the sanitized (non-negative) weight values.

## Failures / Exceptions

- If `BillboardPlacementAreaConfig.create!` raises `ActiveRecord::RecordInvalid` during auto-provisioning on the index action, the error is rescued, a warning is written to the Rails log, and the page continues to render normally with the remaining configs.
- If all selection weights are set to zero, the model logs a warning but does not fail validation; billboard selection behaviour in this case is undefined and left to the caller.
- Placement area values not included in `Billboard::ALLOWED_PLACEMENT_AREAS` are rejected by model validation with an inclusion error.
