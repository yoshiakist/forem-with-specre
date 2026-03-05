---
id: "01KJ029Q7RK57YNH11SH1V2BBB"
name: "user_can_delete_organization"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/organizations_controller.rb`
- `app/controllers/admin/organizations_controller.rb`
- `app/services/organizations/delete.rb`
- `app/workers/organizations/delete_worker.rb`
- `app/helpers/admin/organizations_helper.rb`
- `spec/services/organizations/delete_spec.rb` (Test)
- `spec/workers/organizations/delete_worker_spec.rb` (Test)
- `app/views/mailers/notify_mailer/organization_deleted_email.html.erb` (Template)
- `app/views/mailers/notify_mailer/organization_deleted_email.text.erb` (Template)

## Functional Overview

An organization admin or a Forem admin can delete an organization. The deletion is enqueued as a background job (`Organizations::DeleteWorker`) so that the web request returns immediately with a confirmation flash message. The worker calls `Organizations::Delete` to bulk-remove the organization's notifications, destroy the organization record, and clear the cached organization reference from its articles. When the deletion is initiated by an organization admin (not a Forem admin), the operator's user cache is busted and a confirmation email is sent via `NotifyMailer#organization_deleted_email`. In every case an audit log entry is written under the `user.organization.delete` category. If the organization or operator cannot be found at job execution time, the worker silently returns without performing any action.

## Scenarios

### Organization admin deletes their own organization

1. The organization admin submits a delete request from the organization settings page.
2. The controller looks up the organization by ID and authorizes the action via Pundit; if authorization fails, a `Pundit::NotAuthorizedError` is rescued and the user is redirected back to the settings page with an error flash.
3. `Organizations::DeleteWorker` is enqueued with the organization ID, the current user's ID, and `deleted_by_org_admin: true`.
4. A success flash message is set and the user is redirected to the organization settings list.
5. The worker resolves the organization and operator records; if either is missing it returns early without error.
6. `Organizations::Delete` is called: notifications belonging to the organization are bulk-deleted in batches, the organization record is destroyed, and all of its former articles have their `cached_organization` field cleared to `nil`.
7. Because `deleted_by_org_admin` is `true`, the operator's `organization_info_updated_at` timestamp is touched, the user's edge cache is busted via `EdgeCache::BustUser`, and a deletion confirmation email is sent to the operator via `NotifyMailer#organization_deleted_email`.
8. An `AuditLog` record is created with category `user.organization.delete` and slug `organization_delete`, storing the organization ID and slug.

### Forem admin deletes an organization

1. A Forem admin submits a delete request from the admin panel.
2. The admin controller looks up the organization by ID and enqueues `Organizations::DeleteWorker` with `deleted_by_org_admin: false`.
3. A success flash is set and the admin is redirected to the admin organization URL.
4. On any `StandardError` during the controller action, the error is rescued, an error flash is set, and the admin is redirected to the user organization settings page.
5. The worker resolves both records, calls `Organizations::Delete`, and writes the audit log entry.
6. Because `deleted_by_org_admin` is `false`, no user cache busting or email notification is performed.

### Worker handles missing organization or operator

1. The worker is invoked but the organization ID does not match any existing record.
2. The worker returns immediately without calling the delete service or performing any side effects.
3. Similarly, if the operator user cannot be found, the worker returns early before the delete service is called.

## Design Intent

Deletion is deferred to a background job to avoid blocking the HTTP request while notifications and articles are cleaned up; the worker runs on the `high_priority` queue with up to 10 retries to handle transient failures. The `deleted_by_org_admin` flag allows a single worker implementation to serve both the self-service and admin-initiated paths while keeping post-deletion side effects (cache busting, email) scoped only to the org-admin flow. Errors inside the worker are captured via `ForemStatsClient` and `Honeybadger` so that failures are observable without surfacing to the user.

## Key Members

- `deleted_by_org_admin` (boolean) — passed to the worker to distinguish between an organization admin-initiated deletion and a Forem admin-initiated deletion; controls whether user cache busting and email notification occur.
- `article_ids` (array) — captured on `Organizations::Delete` initialization before the organization is destroyed, used afterwards to clear `cached_organization` on the formerly associated articles.

## Failures / Exceptions

- If Pundit authorization fails in `OrganizationsController#destroy`, the error is rescued and the user is redirected back to the organization settings page with an error flash; no deletion is enqueued.
- If a `StandardError` is raised in `Admin::OrganizationsController#destroy`, it is rescued and redirects the admin to the user organization settings page with an error flash.
- If the organization or operator user cannot be resolved at job execution time, the worker returns silently without any deletion, cache busting, email, or audit log.
- If any error occurs inside the worker after the records are resolved, it is reported to `ForemStatsClient` and `Honeybadger` and the error is re-raised (Sidekiq will retry up to 10 times).
- The admin helper `deletion_modal_error_message` returns an error string if the current user is not a super-admin or if the organization still holds credits, preventing the delete action from being presented in the UI.
