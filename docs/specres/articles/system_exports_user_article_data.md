---
id: "01KJBN50VXFW9TGEC3VZ6TMM8Z"
name: "system_exports_user_article_data"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/services/exporter/articles.rb`
- `app/services/exporter/service.rb`
- `app/workers/export_content_worker.rb`
- `spec/services/exporter/articles_spec.rb` (Test)
- `spec/services/exporter/service_spec.rb` (Test)
- `spec/workers/export_content_worker_spec.rb` (Test)
- `app/views/mailers/notify_mailer/export_email.html.erb` (Template)
- `app/views/mailers/notify_mailer/export_email.text.erb` (Template)

## Functional Overview

When a user requests a content export, the system enqueues an asynchronous Sidekiq job (`ExportContentWorker`) that invokes `Exporter::Service`. The service iterates over all registered exporters (currently `Exporter::Articles` and `Exporter::Comments`), collects their output as named JSON files, compresses everything into a ZIP archive using DEFLATE compression, delivers the archive as an email attachment to the specified address via `NotifyMailer`, and finally records the export timestamp on the user record while clearing the `export_requested` flag. `Exporter::Articles` serializes only a fixed allowlist of attributes (timestamps, URLs, and general article fields) and supports an optional slug filter to restrict the export to a single article.

## Scenarios

### Worker enqueues and delegates to service

1. A caller enqueues `ExportContentWorker` with a user ID and a destination email address.
2. The worker runs on the `medium_priority` queue and looks up the user by ID.
3. If the user is found, the worker instantiates `Exporter::Service` for that user and calls `export` with the email address.
4. If the user ID does not match any record, the worker exits without calling the service.

### Service collects and zips all exported data

1. `Exporter::Service#export` is called with a destination email and an optional per-exporter configuration hash.
2. The service iterates over `EXPORTERS` (`Exporter::Articles`, `Exporter::Comments`), instantiating each and calling `export` with any matching config options.
3. Each exporter returns a hash of filename-to-content pairs; the service merges all of them.
4. The merged files are compressed into a single in-memory ZIP archive (DEFLATE, best compression).

### Service delivers the archive by email

1. After building the ZIP archive, the service rewinds the buffer and passes its raw bytes to `NotifyMailer` as an attachment.
2. `NotifyMailer` delivers one email immediately to the specified address with the archive attached.
3. The service updates the user record: `export_requested` is set to `false` and `exported_at` is set to the current time.

### Articles exporter serializes all user articles

1. `Exporter::Articles#export` is called with no arguments.
2. The exporter fetches all articles belonging to the user in batches, selecting only the allowlisted attributes.
3. The result is serialized to JSON and returned as `{ "articles.json" => <json string> }`.
4. Each article entry includes time fields, URL fields, and general content fields; the `id` column is excluded from the JSON output.

### Articles exporter filters to a single article by slug

1. `Exporter::Articles#export` is called with a `slug:` keyword argument.
2. The exporter restricts the query to articles owned by the user that match the given slug.
3. If no article matches (slug not found or belongs to another user), the JSON array is empty.
4. If a match is found, the JSON array contains exactly that one article with the standard allowlisted fields.

## Failures / Exceptions

- If the user ID passed to `ExportContentWorker` does not exist, the service is never called and no email is sent.
- `ExportContentWorker` is configured with `retry: 10`, so transient failures (network, mail delivery) are retried up to ten times before the job is discarded.
- The `lock: :until_executed` Sidekiq option prevents duplicate jobs for the same arguments from running concurrently.
