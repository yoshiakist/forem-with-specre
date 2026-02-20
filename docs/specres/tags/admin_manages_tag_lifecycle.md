---
id: "01KHYCF2QMAT9AJYWS2C4TWBPE"
name: "admin_manages_tag_lifecycle"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/admin/tags_controller.rb
- app/views/admin/tags/_form.html.erb (Template)
- app/views/admin/tags/edit.html.erb (Template)
- app/views/admin/tags/index.html.erb (Template)
- app/views/admin/tags/new.html.erb (Template)
- spec/requests/admin/tags_spec.rb (Test)

## Functional Overview

`Admin::TagsController` provides a full CRUD interface for administrators to manage tags. Admins can list tags with Ransack-based filtering, create new tags, and update tag metadata including colors, markdown content, badge associations, subforem assignments, and alias configuration. Tag updates are audit-logged and may trigger background retagging when aliases change.

## Scenarios

### Admin lists tags with filtering

1. An authenticated super admin visits the tags index page and receives a 200 response.
2. Tags are paginated at 50 per page and sorted by taggings count descending by default.
3. When no filter is applied, only supported tags are shown by default.
4. Admins can search and filter tags using Ransack query parameters.

### Admin creates a new tag

1. The admin submits a new tag form with a name and optional metadata.
2. The tag name is downcased before saving.
3. On success, the admin is redirected to the tag edit page with a success flash message.
4. On failure, validation errors are displayed and the new form is re-rendered.

### Admin updates tag metadata

1. The admin updates a tag's attributes (colors, markdown, summary, badge, submission template, etc.).
2. The tag name cannot be changed via update (the `name` parameter is not in the permitted list).
3. All tag updates are recorded via `Audit::Logger`.
4. On success, a flash message confirms the update; on failure, error details are shown.

### Admin configures tag alias and triggers retagging

1. When the admin sets the `alias_for` field on a tag, the system enqueues a `Tags::AliasRetagWorker` job.
2. The retagging worker replaces all occurrences of the aliased tag with the preferred tag across tagged content.

### Admin manages subforem assignments

1. When subforem IDs are provided during update, the system creates `TagSubforemRelationship` records for each ID.
2. Existing subforem relationships not included in the submitted IDs are removed.
3. This allows admins to control which subforems a tag appears in.
