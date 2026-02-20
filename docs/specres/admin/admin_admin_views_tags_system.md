---
id: "01KHY7Q15ER20W2SHXMA3WZSKX"
name: "admin_admin_views_tags_system"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/system/admin/admin_views_tags_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Admin` within the admin domain.

### Behavioral Areas

- **Admin updates a tag**: #{admin_tags_path}?q[supported_eq]=true
- **when viewing the default page**: defaults to viewing all tags
- **when viewing supported tags**: defaults to viewing all tags
- **when viewing unsupported tags**: defaults to viewing all tags


## Scenarios

### S-1: defaults to viewing all tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** defaults to viewing all tags

### S-2: defaults to sorting by taggings count, descending

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** defaults to sorting by taggings count, descending

### S-3: can sort by other columns, like tag name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** can sort by other columns, like tag name

### S-4: shows only supported tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows only supported tags

### S-5: #{admin_tags_path}?q[supported_eq]=true

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** #{admin_tags_path}?q[supported_eq]=true

### S-6: shows only unsupported tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows only unsupported tags

### S-7: #{admin_tags_path}?q[supported_eq]=false

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** #{admin_tags_path}?q[supported_eq]=false

