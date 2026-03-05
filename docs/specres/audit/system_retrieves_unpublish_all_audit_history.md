---
id: "01KJ6GNCJ51XS8RDC57VRV43MD"
name: "system_retrieves_unpublish_all_audit_history"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/queries/audit_log/unpublish_alls_query.rb`
- `app/views/admin/users/show/unpublish_logs/_index.html.erb` (Template)
- `spec/queries/audit_log/unpublish_alls_query_spec.rb` (Test)

## Functional Overview

`AuditLog::UnpublishAllsQuery` retrieves the most recent unpublish-all audit log entry for a given user, along with the articles and comments that were targeted by that action. It supports two modes of operation: a lightweight existence check (`exists?`) that queries only whether a matching audit log record is present, and a full data retrieval (`call`) that returns the audit log record, the associated target articles, and the associated target comments. Both modes return a `Result` struct with consistent fields so callers can use the same interface regardless of which mode was invoked.

## Key Members

- `user_id` — the ID of the user whose unpublish-all history is being queried; used to scope all database lookups
- `Result` struct — holds `exists?` (boolean), `audit_log` (the most recent matching record), `target_articles` (articles affected by that action), and `target_comments` (comments affected by that action)

## Scenarios

### Full data retrieval when an unpublish-all audit log exists

1. The caller invokes the query with a user ID.
2. The system searches for audit log entries with slug `api_user_unpublish` or `unpublish_all_articles` whose data includes that user's ID as `target_user_id`, ordering by creation date descending and taking the most recent match.
3. Because a matching record is found, the system fetches the articles referenced in that record's `target_article_ids` that belong to the user, and the comments referenced in `target_comment_ids` that belong to the user.
4. The result reports `exists?` as true and carries the audit log record, the target articles, and the target comments.

### Full data retrieval when no unpublish-all audit log exists

1. The caller invokes the query with a user ID for whom no matching audit log record exists.
2. The system finds no matching audit log entry.
3. The result reports `exists?` as false; the audit log, target articles, and target comments are all absent (nil or empty).

### Lightweight existence check when an audit log exists

1. The caller invokes `exists?` on a new query instance with a user ID.
2. The system checks whether any audit log entry with the relevant slugs references that user ID as `target_user_id`.
3. The result reports `exists?` as true; no article or comment data is fetched.

### Lightweight existence check when no audit log exists

1. The caller invokes `exists?` on a new query instance with a user ID for whom no matching record exists.
2. The system finds no matching audit log entry.
3. The result reports `exists?` as false.
