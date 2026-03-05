---
id: "01KJ162FSS39965A6QK4V78F2H"
name: "system_audits_notification_events"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/services/audit/notification.rb`
- `app/services/audit/event/payload.rb`
- `app/services/audit/helper.rb`
- `app/services/audit/logger.rb`
- `spec/services/audit/notification_spec.rb` (Test)

## Functional Overview

`Audit::Notification` is the central entry point for the audit instrumentation pipeline. It wraps the ActiveSupport Notifications API to publish and consume custom audit events. Callers invoke `notify` with a listener name and a block that populates an `Audit::Event::Payload` object; if no block is given, the call is a no-op. The instrumented event is then picked up by `listen`, which deserializes it into a structured hash and persists it as an `AuditLog` record containing the user, roles, slug, category, and arbitrary data fields.

## Design Intent

The class delegates event transport entirely to `ActiveSupport::Notifications`, keeping the audit subsystem decoupled from direct database writes in the call path. The payload is built inside a block so that callers never construct a raw hash — enforcement of the payload contract is handled by `Audit::Event::Payload`, not by the caller.

## Key Members

- `listener` — the named channel used to scope the instrumentation event; resolved to a full instrument name via `Audit::Helper#instrument_name`
- `Audit::Event::Payload` — the object yielded to the caller's block; enforces the structure of audit event data (user_id, roles, slug, data)

## Scenarios

### Notify with a block — event is published and persisted

1. A caller invokes `Audit::Notification.notify` with a listener name and a block.
2. The block receives an `Audit::Event::Payload` instance and sets fields such as `user_id`, `roles`, and `data`.
3. The system instruments an event on the channel identified by `instrument_name(listener)`, passing the populated payload.
4. `listen` receives the raw ActiveSupport event arguments, reconstructs an `ActiveSupport::Notifications::Event`, extracts fields via `params_hash`, and calls `AuditLog.create!` to persist the record.
5. The resulting `AuditLog` row contains the correct `user_id`, `roles`, `slug`, `category`, and `data`.

### Notify without a block — event is suppressed

1. A caller invokes `Audit::Notification.notify` with a listener name but no block.
2. The system detects the absence of a block and returns immediately.
3. No instrumentation event is fired and `listen` is never called.

### Params hash construction

1. Given an `ActiveSupport::Notifications::Event`, `params_hash` extracts `user_id`, `roles`, `slug`, `data` from the event payload and `name` as the `category`.
2. The resulting hash is passed directly to `AuditLog.create!`.

## Failures / Exceptions

- If `AuditLog.create!` raises (e.g., a validation error or database failure), the exception propagates to the caller; no rescue is performed within `Audit::Notification`.
