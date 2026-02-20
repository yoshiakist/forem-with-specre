---
id: "01KHYAJ5A6WCMJEYQEF12BEETG"
name: "organization_deletion_cleans_associations_and_notifies"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/organizations/delete.rb
- app/workers/organizations/delete_worker.rb
- spec/services/organizations/delete_spec.rb (Test)
- spec/workers/organizations/delete_worker_spec.rb (Test)

## Functional Overview

The organization deletion system consists of a service (Organizations::Delete) that handles data cleanup and a high-priority Sidekiq worker (Organizations::DeleteWorker) that orchestrates the full deletion flow including notification emails, user cache busting, and audit logging.

## Scenarios

### Service deletes organization and cleans up associations

1. The service batch-deletes all notifications belonging to the organization using `BulkSqlDelete`.
2. The service destroys the organization record, cascading to dependent associations.
3. The service nullifies `cached_organization` on all formerly-associated articles.

### Worker orchestrates deletion with notification and audit

1. The worker looks up the organization and operator user by ID; exits silently if either is not found.
2. The worker calls `Organizations::Delete` to perform the actual deletion.
3. If the deletion was initiated by an org admin (`deleted_by_org_admin` is true), the worker touches the user's `organization_info_updated_at`, busts the user's edge cache, and sends an `organization_deleted_email` via `NotifyMailer`.
4. The worker creates an `AuditLog` entry with category "user.organization.delete" and the organization's ID and slug.

### Worker handles errors gracefully

1. If an error occurs, the worker reports a failure metric via `ForemStatsClient`, adds context to Honeybadger, and re-notifies the exception.
2. The worker is configured for high priority with up to 10 retries.
