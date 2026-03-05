---
id: "01KJ6E7W8QWARD67FEGBQWTH1T"
name: "system_tracks_billboard_events"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/billboard_events_controller.rb`
- `app/models/billboard_event.rb`
- `spec/controllers/billboard_events_controller_spec.rb` (Test)
- `spec/requests/billboard_events_spec.rb` (Test)
- `spec/models/billboard_event_spec.rb` (Test)

## Functional Overview

When a billboard is displayed or interacted with, the system records a `BillboardEvent` associating the event with a billboard, the current user, and an optional article context along with the user's geolocation. The controller accepts both a current and a legacy parameter format (`display_ad_event`) for backward compatibility with cached JavaScript payloads. After persisting the event, the system enqueues `Billboards::DataUpdateWorker` via a throttled call (defaulting to 25 minutes) to update aggregate billboard data, unless disabled via the `DISABLE_BILLBOARD_DATA_UPDATE` application config flag. The endpoint always responds with HTTP 200.

## Key Members

- `THROTTLE_TIME` — default 25-minute throttle window for billboard data update jobs; overridable via the `BILLBOARD_EVENT_THROTTLE_TIME` config key
- `VALID_CATEGORIES` — `impression`, `click`, `signup`, `conversion`
- `VALID_CONTEXT_TYPES` — `home`, `article`, `email`

## Scenarios

### Recording an impression or click event

1. A client posts to `POST /billboard_events` with a `billboard_event` payload specifying `billboard_id`, `context_type`, and `category` (e.g., `impression` or `click`).
2. The system merges the current user's ID and geolocation into the event parameters, then persists a `BillboardEvent` record.
3. The system enqueues `Billboards::DataUpdateWorker` for the billboard via a throttled call, so repeated events within the throttle window do not spawn redundant jobs.
4. The endpoint responds with HTTP 200.

### Recording a signup or conversion event

1. A client posts a `billboard_event` with `category` set to `signup` or `conversion`.
2. The model validates that the user has not already recorded a conversion event of the same category; if they have, the record is invalid and an error is added.
3. For `signup` events, the model additionally validates that the user registered within the last 24 hours; events from older accounts are rejected.
4. If validations pass, the event is persisted and the data update worker is enqueued as above.

### Accepting legacy parameter format

1. A client posts using the legacy `display_ad_event` key (from old cached JavaScript) instead of `billboard_event`, and may also supply `display_ad_id` instead of `billboard_id`.
2. The controller normalizes these to the current parameter names before creating the event, ensuring continuity with cached clients.

### Skipping data update when disabled

1. The `DISABLE_BILLBOARD_DATA_UPDATE` application config is set to `"yes"`.
2. A `BillboardEvent` is still created and persisted normally.
3. The system skips enqueuing `Billboards::DataUpdateWorker`, preventing any aggregate data refresh.

## Failures / Exceptions

- A user who has already recorded a `signup` or `conversion` event for a billboard cannot record another; the model adds an `"has already converted"` error on `user_id` and the record is not saved.
- A `signup` event from a user whose `registered_at` is more than 24 hours in the past is rejected with an `"is not a recent registration"` error on `user_id`.
- Events with a `category` or `context_type` outside the defined valid sets are rejected by model validations.
