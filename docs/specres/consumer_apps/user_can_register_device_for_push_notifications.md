---
id: "01KJ3YY1P1TX3DWW24AABW70MT"
name: "user_can_register_device_for_push_notifications"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/devices_controller.rb`
- `spec/requests/devices_spec.rb` (Test)

## Functional Overview

When an authenticated user submits a device token, platform identifier, and app bundle from a mobile consumer app, the system registers the device for push notifications by finding or creating a `Device` record associated with the current user and a matching `ConsumerApp`. If the device is successfully persisted, the system responds with the new device's ID and a `201 Created` status to confirm registration. If the device cannot be persisted due to invalid parameters (such as an unrecognized platform), the system responds with validation errors and a `400 Bad Request` status. Any unexpected database or argument errors are caught globally and return a `422 Unprocessable Entity` response.

## Design Intent

Device registration uses `find_or_create_by` to make the operation idempotent — submitting the same token and platform from the same app will not create duplicate device records. Authentication is enforced implicitly through the `Device` model's `belongs_to :user` association rather than a controller-level filter, replacing a previous Pusher Beams integration. Returning the internal device ID in the success response acts as a confirmation receipt for the consumer app, even if the ID is not otherwise used on the client side.

## Key Members

- `token` — the push notification token issued by the platform (e.g., APNs or FCM) uniquely identifying the device
- `platform` — the mobile platform identifier (e.g., `"ios"`, `"android"`); must be a recognized value or validation fails
- `app_bundle` — the bundle ID used to look up the associated `ConsumerApp` record

## Scenarios

### Successful device registration

1. An authenticated user sends a `POST /users/devices` request with a valid push notification token, a recognized platform value, and a valid app bundle identifier.
2. The system resolves the `ConsumerApp` matching the given app bundle and platform.
3. The system finds an existing `Device` record matching all parameters, or creates a new one associated with the current user.
4. The device is persisted successfully, and the system responds with the device's ID and a `201 Created` status.

### Duplicate registration is idempotent

1. An authenticated user sends a `POST /users/devices` request for a device that is already registered (same token, platform, app bundle, and user).
2. The system finds the existing `Device` record via `find_or_create_by` and does not create a duplicate.
3. The system responds with the existing device's ID and a `201 Created` status.

### Registration fails with an invalid platform

1. An authenticated user sends a `POST /users/devices` request with an unrecognized platform value.
2. The `Device` model validation fails and the record is not persisted.
3. The system responds with a descriptive validation error message and a `400 Bad Request` status.

## Failures / Exceptions

- If a database error (`ActiveRecord::ActiveRecordError`) or an argument error occurs during registration, the controller's rescue handler returns a JSON error body with a `422 Unprocessable Entity` status.
- If the submitted platform is not among the accepted values, model validation fails and a `400 Bad Request` is returned with a human-readable error sentence.
