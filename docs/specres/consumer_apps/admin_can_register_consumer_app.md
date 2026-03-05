---
id: "01KJ3YXYAR6AARATJH02XHAEVW"
name: "admin_can_register_consumer_app"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/admin/consumer_apps_controller.rb`
- `app/javascript/admin/controllers/consumer_app_controller.js`
- `app/models/consumer_app.rb`
- `app/policies/consumer_app_policy.rb`
- `app/queries/consumer_apps/find_or_create_all_query.rb`
- `app/views/admin/consumer_apps/_form.html.erb` (Template)
- `app/views/admin/consumer_apps/edit.html.erb` (Template)
- `app/views/admin/consumer_apps/index.html.erb` (Template)
- `app/views/admin/consumer_apps/new.html.erb` (Template)
- `spec/requests/admin/consumer_apps_spec.rb` (Test)
- `spec/models/consumer_app_spec.rb` (Test)
- `spec/queries/consumer_apps/find_or_create_all_query_spec.rb` (Test)
- `spec/factories/consumer_apps.rb` (Test)

## Functional Overview

Administrators (super admins and single-resource admins scoped to `ConsumerApp`) can register, update, and remove mobile consumer apps via the Admin dashboard. A consumer app represents a mobile client (iOS or Android) identified by an app bundle identifier and a platform, along with authentication credentials used for push notification delivery. The index page auto-ensures that the two built-in Forem platform apps (`com.forem.app` for iOS and Android) always exist via `ConsumerApps::FindOrCreateAllQuery`, creating any that are missing. Creator-registered apps (any app whose bundle differs from `com.forem.app`) are fully manageable through the admin UI, while the built-in Forem apps are displayed read-only. The policy layer (`ConsumerAppPolicy`) prevents any mutation of the built-in Forem apps by checking `creator_app?` on every write action.

## Design Intent

The `FindOrCreateAllQuery` pattern guarantees the two built-in Forem apps are always present without requiring a database seed or migration, making the index page self-healing. Credentials for Forem apps are read from environment variables rather than the database, so they are never editable through the UI — only creator apps store credentials in `auth_key`. The Stimulus controller (`ConsumerAppController`) conditionally reveals the Team ID field only when the iOS platform is selected, keeping the form clean for Android-only registrations.

## Key Members

- `app_bundle` — reverse-domain identifier for the mobile app (e.g., `com.example.myapp`); must be unique per platform
- `platform` — enum: `ios` or `android`
- `auth_key` — push-notification credential stored in the database; used only for creator apps
- `active` — boolean flag; a `ConsumerApp` is `operational?` only when both `active` is true and `auth_credentials` are present
- `ConsumerApp::FOREM_BUNDLE` — `"com.forem.app"`, the reserved bundle for built-in Forem apps
- `ConsumerApp::FOREM_APP_PLATFORMS` — `["ios", "android"]`, the two supported built-in platforms

## Scenarios

### Admin views the consumer apps index

1. An admin navigates to the Consumer Apps admin page.
2. The system calls `ConsumerApps::FindOrCreateAllQuery`, which checks whether a `ConsumerApp` record exists for each entry in `FOREM_APP_PLATFORMS` with the `FOREM_BUNDLE`. Any missing built-in apps are created with the `FOREM_TEAM_ID`.
3. The page renders all consumer apps (up to 50) in a table showing app bundle, platform, device count, authentication key availability, and operational status.
4. Built-in Forem apps show a read-only note; creator apps show Edit and Destroy action links.

### Admin registers a new creator app

1. An admin clicks "New Consumer App" and is presented with a form containing fields for app bundle, platform, and authentication key.
2. When the iOS platform is selected, the Stimulus controller (`ConsumerAppController`) reveals the Team ID field; for Android it remains hidden.
3. The admin submits the form. The system builds a new `ConsumerApp` from the permitted params (`app_bundle`, `platform`, `auth_key`) and checks the policy to confirm it is a creator app.
4. If the record saves successfully, a success flash message is shown and the admin is redirected to the index page.
5. If validation fails (e.g., duplicate app bundle and platform combination, missing app bundle), the form is re-rendered with an error message.

### Admin updates an existing creator app

1. An admin clicks "Edit" on a creator app row and is presented with the pre-filled edit form.
2. The system loads the `ConsumerApp` by ID and authorizes that it is a creator app, not a built-in Forem app.
3. The admin modifies fields and submits. The system updates the record.
4. On success, a success flash is shown and the admin is redirected to the index. On failure, the edit form is re-rendered with an error.
5. After the update, the `clear_rpush_app` callback destroys the stale Redis-backed Rpush app entry so it will be recreated with fresh credentials on the next push.

### Admin deletes a creator app

1. An admin clicks "Destroy" on a creator app row and confirms the prompt.
2. The system loads the `ConsumerApp` by ID and authorizes that it is a creator app.
3. The record is destroyed along with all associated `Device` records (via `dependent: :destroy`).
4. On success, a success flash is shown and the admin is redirected to the index.

## Failures / Exceptions

- A non-admin user or a single-resource admin scoped to a different resource receives a `Pundit::NotAuthorizedError` on any request to the consumer apps admin routes.
- Any attempt to create or modify a built-in Forem app (`forem_app? == true`) is blocked by `ConsumerAppPolicy`, which restricts all write actions to creator apps.
- Creating a `ConsumerApp` with a duplicate `app_bundle` + `platform` combination fails model validation; the form is re-rendered with the validation errors displayed.
- If `FindOrCreateAllQuery` fails to auto-create a missing Forem app (e.g., due to a database error), the error is caught, incremented in `ForemStatsClient` under the `consumer_apps.create` metric, and the index continues to load with whatever apps are available.
