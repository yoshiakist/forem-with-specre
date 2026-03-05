---
id: "01KJ6GMNB25T18H7JGRZFEBQH5"
name: "system_subscribes_to_audit_event_channels"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/audit/subscribe.rb`
- `app/services/audit/helper.rb`
- `spec/services/audit/subscribe_spec.rb` (Test)
- `spec/services/audit/helper_spec.rb` (Test)

## Functional Overview

The system provides a mechanism to register and deregister named listeners on audit event channels using `ActiveSupport::Notifications`. The `Audit::Subscribe` class exposes two class-level methods, `listen` and `forget`, which accept one or more listener names and map each to a notification channel by appending the `.audit.log` suffix (defined in `Audit::Helper`). When a listener is registered, any notification fired on its channel is forwarded to `Audit::Notification.listen` for processing. The suffix is provided by `Audit::Helper#instrument_name`, which is included as a module in `Audit::Subscribe`.

## Design Intent

Appending a consistent `.audit.log` suffix to all channel names namespaces audit-related notifications, preventing name collisions with other `ActiveSupport::Notifications` channels in the application. Delegating channel name construction to a shared `Audit::Helper` module keeps the naming convention DRY and easy to change in one place.

## Key Members

- `NOTIFICATION_SUFFIX` — the string `.audit.log` appended to every listener name to form the full notification channel name.

## Scenarios

### System registers a listener on an audit channel

1. A caller invokes `Audit::Subscribe.listen` with one or more listener names (e.g., `:moderator`, `:visitor`).
2. For each name, the system constructs the full notification channel name by appending the `.audit.log` suffix.
3. The system subscribes to each channel via `ActiveSupport::Notifications`, routing incoming events to `Audit::Notification.listen`.

### System registers multiple listeners in a single call

1. A caller passes several listener names to `Audit::Subscribe.listen` at once.
2. The system iterates over each name and subscribes each to its corresponding `.audit.log` channel independently.
3. All named channels become active simultaneously after the call returns.

### System deregisters a listener from an audit channel

1. A caller invokes `Audit::Subscribe.forget` with one or more listener names.
2. For each name, the system constructs the full channel name using the `.audit.log` suffix.
3. The system unsubscribes from each channel via `ActiveSupport::Notifications`, stopping further event delivery to `Audit::Notification.listen` for those channels.
