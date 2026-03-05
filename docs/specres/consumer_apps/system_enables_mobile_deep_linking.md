---
id: "01KJ3YY715791TP7N04ECPMPGV"
name: "system_enables_mobile_deep_linking"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/deep_links_controller.rb`
- `spec/requests/universal_links_spec.rb` (Test)

## Functional Overview

The system exposes two endpoints to support mobile deep linking. The `mobile` action renders a landing page for users arriving via a mobile deep link. The `aasa` action generates and serves an Apple App Site Association (AASA) JSON file at `/.well-known/apple-app-site-association`, which iOS devices fetch to verify that the web domain is authorized to open associated native apps. The AASA payload is built dynamically by querying all registered iOS consumer apps via `ConsumerApps::FindOrCreateAllQuery`, combining each app's `team_id` and `app_bundle` into a fully-qualified Apple App ID, and projecting those IDs into the required `applinks`, `activitycontinuation`, and `webcredentials` structures. Only iOS apps with a non-null `team_id` are included. All deep link paths are allowed except authentication routes.

## Design Intent

The AASA file is constructed dynamically rather than statically so that any iOS consumer app registered in the system is automatically included in universal link support without requiring a manual configuration file update. The constant `AASA_PATHS` captures the path allowlist in a single place, making the scope of deep linking easy to review and adjust.

## Key Members

- `AASA_PATHS` — frozen array of path patterns included in every app's `paths` field; currently allows all paths (`/*`) while explicitly excluding authentication routes (`NOT /users/auth/*`)

## Scenarios

### Serving the AASA file with multiple registered iOS apps

1. An iOS device requests `/.well-known/apple-app-site-association` to validate universal links for the domain.
2. The system queries all consumer apps via `ConsumerApps::FindOrCreateAllQuery`, filters to iOS platform, and excludes any records missing a `team_id`.
3. Each qualifying record's `team_id` and `app_bundle` are joined with a dot to form a valid Apple App ID (e.g., `TEAM1.com.example.app`).
4. The system responds with HTTP 200 and a JSON body containing `applinks`, `activitycontinuation`, and `webcredentials` sections, each listing all qualifying app IDs. The `applinks.details` array maps every app ID to `AASA_PATHS`.

### Serving the AASA file with no custom consumer apps registered

1. No custom consumer apps exist in the database.
2. `ConsumerApps::FindOrCreateAllQuery` creates or returns the default Forem app record.
3. The system responds with a valid AASA JSON body that references only the default Forem app ID.

### Serving the AASA file on a non-public Forem instance

1. The Forem instance is configured as non-public (`Settings::UserExperience.public` is false).
2. A request to `/.well-known/apple-app-site-association` is made.
3. The system responds with HTTP 200 and a valid AASA JSON body regardless of the instance's public visibility setting, ensuring deep linking continues to work on private communities.

### Mobile deep link landing page

1. A user follows a universal link or deep link that resolves to the `mobile` action.
2. The system renders the associated mobile landing view, which can guide the user to open or install the native app.

## Failures / Exceptions

- Apps registered with a `null` `team_id` are silently excluded from the AASA output; no error is raised and they do not appear in the JSON response.
- Android consumer apps are excluded from the AASA response because the query filters strictly to `Device::IOS`; their presence in the database has no effect on the output.
