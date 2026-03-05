---
id: "01KJ5DKW47KSVWWH6R13NNG8EM"
name: "user_exports_own_comments"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/services/exporter/comments.rb`
- `spec/services/exporter/comments_spec.rb` (Test)

## Functional Overview

`Exporter::Comments` produces a JSON export of all comments belonging to a given user. When initialized with a user, the service retrieves that user's comments from the database, optionally filtering to a single comment identified by its `id_code`. Each exported comment record includes a fixed set of content and metadata fields, and is augmented with the URL path of its commentable resource (article, podcast episode, or other polymorphic target). The result is returned as a hash with a single `"comments.json"` key whose value is a JSON string.

## Key Members

- `name` — fixed symbol `:comments`, used as the export filename stem.
- `user` — the user whose comments are exported; all queries are scoped to this user.
- `id_code` — optional filter passed to `export`; when present, limits the result to the single comment with that code.
- Exported fields per comment: `body_markdown`, `created_at`, `deleted`, `edited`, `edited_at`, `id_code`, `markdown_character_count`, `public_reactions_count`, `processed_html`, `receive_notifications`, and `commentable_path`.

## Scenarios

### Export all comments for a user

1. Caller creates an `Exporter::Comments` instance for a specific user.
2. Caller invokes `export` with no arguments.
3. The service fetches every comment owned by that user, eager-loading each comment's associated commentable resource.
4. Each comment is serialized with the allowed metadata fields plus the path of its commentable.
5. The result is returned as `{ "comments.json" => <JSON string> }` containing all comments.

### Export a single comment by id_code

1. Caller invokes `export` with a known `id_code`.
2. The service scopes the query to only the comment with that `id_code` among the user's comments.
3. The matching comment is serialized the same way as in the full export.
4. The result contains exactly one comment entry.

### id_code filter returns no results when code is unknown

1. Caller invokes `export` with an `id_code` that does not match any comment in the system.
2. The service finds no matching comments.
3. The result contains an empty JSON array.

### id_code filter returns no results when code belongs to another user

1. Caller invokes `export` with an `id_code` that belongs to a comment created by a different user.
2. Because queries are scoped to the initialized user, the comment is not found.
3. The result contains an empty JSON array, preventing cross-user data leakage.

### commentable_path reflects the linked resource

1. A comment is associated with an article or a podcast episode.
2. The service eager-loads the commentable association to avoid N+1 queries.
3. The path of the commentable is merged into the comment's JSON as `commentable_path`.
4. If the commentable has been deleted or is nil, `commentable_path` is `null`.
