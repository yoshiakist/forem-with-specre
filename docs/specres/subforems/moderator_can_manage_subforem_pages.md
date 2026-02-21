---
id: "01KHYH5N8Y83SD7G7S5DDF7ZJZ"
name: "moderator_can_manage_subforem_pages"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/subforems_controller.rb
- app/views/subforems/new_page.html.erb (Template)
- app/views/subforems/edit_page.html.erb (Template)
- spec/requests/subforems_spec.rb (Test)

## Functional Overview

Subforem moderators, super moderators, and admins can create, edit, and delete custom pages within a subforem. Pages have a title, slug, description, body written in Markdown, and an optional social image. Pages can be designated as top-level (accessible at the subforem root path) or nested under a slug. The page management interface is accessed from the subforem edit page's "Pages" section.

## Scenarios

### Moderator creates a new page

1. Moderator clicks "Create New Page" from the subforem edit page
2. System renders the new page form with fields for title, slug, description, body markdown, and social image
3. Moderator fills in the required fields and submits
4. System creates the `Page` record associated with the subforem and redirects to the subforem edit page

### Moderator edits an existing page

1. Moderator clicks the edit link next to a page in the Pages section
2. System renders the edit form pre-filled with the page's current content
3. Moderator updates the desired fields and submits
4. System persists the changes and redirects to the subforem edit page

### Moderator deletes a page

1. Moderator clicks the delete button next to a page in the Pages section
2. System destroys the `Page` record
3. Moderator is redirected to the subforem edit page

### Authorization gates page management

1. Only users with `create_page?`, `update_page?`, or `destroy_page?` permissions (super admin, super moderator, or subforem moderator) can manage pages
2. Regular users receive a forbidden response
