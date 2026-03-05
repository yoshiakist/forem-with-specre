---
id: "01KJ41VY1GJ0K2GW8VGQXEA5NR"
name: "admin_can_view_tag_list"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/controllers/admin/tags_controller.rb`
- `app/views/admin/tags/index.html.erb` (Template)
- `spec/requests/admin/tags_spec.rb` (Test)
- `spec/system/admin/admin_views_tags_spec.rb` (Test)

## Functional Overview

When an admin navigates to the tags index, the system applies default search options before rendering the list: if no search query is present, it scopes results to tags where `supported` is not null, and always defaults sorting to taggings count descending. The resulting paginated list (50 per page) is built via `Tag.ransack`, and the view presents tabs for filtering by All, Supported, or Unsupported tags, a name search field, sortable column headers (name, id, alias_for, taggings_count), and a link to create a new tag.

## Design Intent

The `set_default_options` callback ensures that admins always land on a meaningful, pre-filtered and pre-sorted view without requiring explicit query parameters, reducing friction for the common case of browsing the most-used tags first.

## Key Members

- `@q` — Ransack search object built from `params[:q]`; used by the view to render the search form and sort links
- `@tags` — Paginated result set (50 per page), derived from `@q.result`
- Default scope: `supported_not_null: "true"` when no query params are given
- Default sort: `taggings_count desc` when no sort param is given

## Scenarios

### Viewing the tag list with default options

1. An authenticated admin navigates to `GET /admin/content_manager/tags` without any query parameters.
2. The system sets the search scope to tags where `supported` is not null and the sort order to taggings count descending.
3. The first page of up to 50 matching tags is rendered, sorted by most-tagged first.

### Filtering tags by supported status

1. An admin clicks the "Supported" or "Unsupported" tab, or navigates with `q[supported_eq]=true` or `q[supported_eq]=false` in the query string.
2. The system passes the parameter through to `Tag.ransack` without applying the default scope.
3. Only tags matching the requested supported status are displayed.

### Searching tags by name

1. An admin types a partial name into the search field and submits the form.
2. The current tab filter (supported/unsupported/all) is preserved via a hidden field in the form.
3. The system filters results using a name contains (`name_cont`) predicate and renders only the matching tags.

### Sorting the tag list by column

1. An admin clicks a sortable column header (Name, ID, Alias For, or Taggings Count).
2. The system re-runs the ransack query with the updated sort parameter and renders the list in the new order.
