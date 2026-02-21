---
id: "01KHZFKZ6V29C5PQ9EM27TMC1G"
name: "system_re_renders_pages_from_template"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/workers/page_templates/re_render_pages_worker.rb`
- `app/models/page.rb`
- `spec/workers/page_templates/re_render_pages_worker_spec.rb` (Test)

## Functional Overview

When a `PageTemplate` changes, the system needs to propagate those changes to all pages that use it. `PageTemplates::ReRenderPagesWorker` is a Sidekiq background job that accepts a `page_template_id`, looks up the template, and iterates over every associated page to call `re_render_from_template!` on each one. The `Page` model's `re_render_from_template!` method delegates to the private `render_from_page_template` callback, which renders the template with the page's own `template_data` and persists the resulting HTML. The worker runs with a concurrency limit of 1 to prevent multiple simultaneous re-render sweeps, uses a medium-priority queue with up to 3 retries, and isolates per-page failures so that one failing page does not abort the entire batch.

## Design Intent

Per-page error isolation via a `rescue StandardError` inside the `find_each` loop ensures that a single corrupt or problematic page cannot block the remaining pages in the batch from being updated. This approach prioritizes eventual consistency across the template's pages over strict atomicity.

## Key Members

- `page_template_id` — the ID of the `PageTemplate` whose associated pages should be re-rendered; the worker exits early without error if no matching template is found
- `template_data` — a hash of values stored on each `Page` that are merged into the template when rendering

## Scenarios

### Re-rendering all pages for a changed template

1. A caller enqueues `PageTemplates::ReRenderPagesWorker` with a valid `page_template_id`.
2. The worker looks up the `PageTemplate` by that ID.
3. For each page associated with the template, the worker calls `re_render_from_template!`.
4. `re_render_from_template!` verifies the page still references a template, then renders the template using the page's `template_data` and saves the resulting `processed_html` back to the page.
5. All associated pages now reflect the latest template content.

### Template not found

1. A caller enqueues the worker with a `page_template_id` that does not exist (for example, because the template was deleted).
2. The worker looks up the template and finds nothing.
3. The worker returns immediately without performing any work and without raising an error.

### One page fails during batch processing

1. The worker begins iterating over the pages for a valid template.
2. One page raises a `StandardError` during `re_render_from_template!`.
3. The worker logs the error (including the page ID and template ID) and moves on to the next page.
4. All other pages in the batch are re-rendered successfully.

## Failures / Exceptions

- If `re_render_from_template!` raises a `StandardError` for any individual page, the error is caught, logged via `Rails.logger.error`, and iteration continues with the remaining pages.
