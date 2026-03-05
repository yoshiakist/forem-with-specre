---
id: "01KHZFCE4EMXDS8J8BCARX9EQW"
name: "admin_can_manage_pages"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/admin/pages_controller.rb`
- `app/models/page.rb`
- `app/workers/pages/bust_cache_worker.rb`
- `app/views/admin/pages/index.html.erb` (Template)
- `app/views/admin/pages/new.html.erb` (Template)
- `app/views/admin/pages/edit.html.erb` (Template)
- `app/views/admin/pages/_form.html.erb` (Template)
- `app/views/admin/pages/_landing_page_modal.html.erb` (Template)
- `spec/requests/admin/pages_spec.rb` (Test)
- `spec/system/admin/admin_manages_pages_spec.rb` (Test)
- `spec/workers/pages/bust_cache_worker_spec.rb` (Test)
- `spec/factories/pages.rb` (Test)

## Functional Overview

Administrators can create, view, edit, and delete custom static pages within the Forem platform. Each page has a slug, title, description, body content (in markdown, HTML, JSON, or CSS), and a layout template type. Pages may optionally be bound to a `PageTemplate`, in which case body content is generated from structured template fields rather than entered manually. The index view groups pages by subforem and surfaces quick-override links for the three default system pages (code of conduct, privacy policy, terms of use). On every save, `Pages::BustCacheWorker` asynchronously invalidates the page's edge-cache entry via `EdgeCache::BustPage`. If a page is designated the landing page for a private Forem instance, the system enforces the invariant that at most one landing page may exist at a time by unsetting the flag on all other pages after commit.

## Design Intent

The three system pages (code of conduct, privacy policy, terms of use) are managed by Forem centrally by default. The admin UI deliberately surfaces them in a separate "Override defaults" section with a warning so administrators understand that creating a custom version opts them out of future Forem-managed updates. The fork mechanism (`?page=<id>`) lets administrators duplicate an existing page including its template relationship, reducing the cost of creating similar pages. Slug uniqueness is validated cross-model (against `User`, `Organization`, and `Podcast` slugs) to prevent routing collisions.

## Key Members

- `TEMPLATE_OPTIONS` — allowed layout types: `contained`, `full_within_layout`, `nav_bar_included`, `json`, `css`, `txt`
- `CODE_OF_CONDUCT_SLUG`, `PRIVACY_SLUG`, `TERMS_SLUG` — reserved slug constants for default system pages
- `PAGE_DIRECTORY_LIMIT` — maximum number of `/`-separated path segments allowed in a slug (6)
- `PAGE_ALLOWED_PARAMS` — controller-level allowlist of permitted page attributes

## Scenarios

### Listing pages

1. An admin visits the pages index at `/admin/customization/pages`.
2. The system displays all pages scoped to the current subforem, ordered by creation date, along with any associated page template name.
3. If any page templates exist, an informational tip is shown encouraging their use.
4. System pages not yet overridden (code of conduct, privacy policy, terms of use) appear in an "Override defaults" section with a caution notice. If all three have been overridden, a different notice explains that updates from Forem will no longer be received.

### Creating a new page

1. An admin clicks "New page" and the form opens with empty fields.
2. The admin fills in title, slug, description, and selects a layout template type and body content (markdown, HTML, JSON, or CSS depending on the template type).
3. On submit, the system validates presence of title and description, that at least one body field is populated (unless a `PageTemplate` is used), that the slug is unique across pages within the same subforem and does not conflict with user, organization, or podcast slugs, and that the slug does not start with `sitemap-` or exceed `PAGE_DIRECTORY_LIMIT` directory segments.
4. On success, the page is saved, the edge cache is busted asynchronously, and the admin is redirected to the index with a success flash.
5. On failure, the form re-renders with validation errors displayed.

### Creating a page from a template

1. An admin selects a `PageTemplate` (either from the new-page form via `?page_template_id=<id>` or by clicking a template link).
2. The form shows template-specific fields defined by the template's schema instead of free-form body inputs.
3. On submit, `template_data` is parsed from the structured parameters and stored on the page; `render_from_page_template` generates `processed_html` and sets the template type from the `PageTemplate`.
4. On success the page is saved and the admin is redirected to the index.

### Editing and updating a page

1. An admin clicks "Edit" next to a page in the index.
2. The existing page attributes are pre-populated in the form. If the Forem instance is private, a "Use as Locked Screen" checkbox is shown.
3. If the landing-page checkbox is checked and another landing page already exists, a confirmation modal prompts the admin to overwrite the current locked screen.
4. On save, the system validates the same rules as creation; success redirects to the index, failure re-renders the edit form with errors.
5. After a successful save, the edge cache for the page's slug is busted asynchronously.

### Deleting a page

1. An admin opens the edit form and clicks "Delete Page".
2. The system destroys the page record and redirects to the index with a success flash.

### Forking an existing page

1. An admin clicks "Fork" next to a page in the index; the new-page form opens pre-populated with a duplicate of the original page's attributes.
2. If the original page was created from a `PageTemplate`, the fork preserves the template relationship and copies `template_data`.
3. The admin adjusts the slug and any other fields, then saves as a new page.

### Overriding a default system page

1. An admin clicks "Override" next to a default system page (code of conduct, privacy policy, or terms of use).
2. The new-page form opens pre-populated with the slug, a default title, description, and rendered HTML body for that system page.
3. The admin adjusts content and saves; the new page then appears in the main pages table and the override section disappears for that entry.

### Cache busting after page save

1. After any page save (create or update), the `after_commit` callback enqueues `Pages::BustCacheWorker` with the page's slug.
2. The worker calls `EdgeCache::BustPage.call(slug)` to purge the cached response.
3. If the slug is blank the worker returns early without calling the cache buster.

## Failures / Exceptions

- Saving fails if `title` or `description` is blank.
- Saving fails if no body field is provided and the page does not use a `PageTemplate`.
- Saving fails if the slug duplicates an existing page slug within the same subforem, or conflicts with a `User`, `Organization`, or `Podcast` slug.
- Saving fails if the slug begins with `sitemap-` or contains more than `PAGE_DIRECTORY_LIMIT` (6) subdirectory segments.
- Saving fails if `template_data` does not satisfy the `PageTemplate`'s schema validation.
- If a non-existent page ID is passed to `?page=<id>` when forking, the form opens blank instead of raising an error.
