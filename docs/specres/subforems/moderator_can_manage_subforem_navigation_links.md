---
id: "01KHYH6H3EC7J6FS17BS9ZBE0F"
name: "moderator_can_manage_subforem_navigation_links"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/subforems_controller.rb
- spec/requests/subforems_spec.rb (Test)
- spec/views/subforems/edit_spec.rb (Test)

## Functional Overview

Subforem moderators, super moderators, and admins can create, update, and delete custom navigation links for a subforem. Each navigation link has a name, URL, an optional uploaded image, and an optional inline SVG icon. Navigation links appear in the subforem's sidebar or header navigation. After any change, the system busts the edge cache for the navigation links to ensure visitors see the updated navigation immediately.

## Scenarios

### Moderator creates a navigation link

1. Moderator opens the "Navigation Links" section on the subforem edit page
2. Moderator fills in the name, URL, and optionally uploads an image or provides an SVG icon
3. System creates the `NavigationLink` record associated with the subforem
4. System busts the edge cache for the subforem's navigation links
5. Moderator sees the new link listed in the Navigation Links section

### Moderator updates a navigation link

1. Moderator clicks edit on an existing navigation link
2. Moderator modifies the name, URL, image, or SVG icon
3. System persists the changes and busts the edge cache
4. The edit form displays an image preview when the link already has an uploaded image

### Moderator deletes a navigation link

1. Moderator clicks the delete button next to a navigation link
2. System destroys the `NavigationLink` record and busts the edge cache
3. Moderator is redirected to the subforem edit page

### Image upload field ordering

1. The create and edit forms display the image upload field before the SVG icon field
2. The SVG icon field is hidden by default with a toggle button to reveal it
3. Each link's edit form has a unique toggle function to avoid conflicts
