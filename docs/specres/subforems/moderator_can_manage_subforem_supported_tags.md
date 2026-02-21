---
id: "01KHYY9VPHV3N120R4QWFZ0SYK"
name: "moderator_can_manage_subforem_supported_tags"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/subforems_controller.rb
- spec/requests/subforems_spec.rb (Test)
- spec/factories/tag_subforem_relationships.rb (Test)

## Functional Overview

Subforem moderators, super moderators, and admins can add or remove tags from a subforem's supported tag list. Adding a tag creates a `TagSubforemRelationship` join record; removing a tag destroys it. These operations are performed via AJAX from the "Supported Tags" section of the subforem edit page and return JSON responses. The supported tags determine which content categories are visible and encouraged within the subforem.

## Scenarios

### Moderator adds a tag to the subforem

1. Moderator types a tag name in the "Supported Tags" input on the subforem edit page
2. System sends a JSON request to the `add_tag` action
3. System creates a `TagSubforemRelationship` linking the tag to the subforem
4. System responds with a JSON success message

### Moderator removes a tag from the subforem

1. Moderator clicks the remove button next to a tag in the supported tags list
2. System sends a JSON request to the `remove_tag` action
3. System destroys the `TagSubforemRelationship` record
4. System responds with a JSON success message

### Authorization gates tag management

1. Only users with `add_tag?` or `remove_tag?` permissions can manage supported tags
2. Regular users receive a forbidden response
