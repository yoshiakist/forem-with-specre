---
id: "01KHY7Q106VNZAQYVWT15HEEW0"
name: "admin_articles_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/articles_spec.rb

## Functional Overview

This specification defines the expected behavior of `"/admin/content_manager/articles"` within the admin domain.

### Behavioral Areas

- **/admin/content_manager/articles**: Ensures correct behavior under the specified conditions
- **when updating an article via /admin/content_manager/articles**: allows an Admin to add a co-author to an individual article
- **when unpinning an article**: allows an Admin to add a co-author to an individual article


## Scenarios

### S-1: allows an Admin to add a co-author to an individual article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows an Admin to add a co-author to an individual article

### S-2: allows an Admin to add co-authors to an individual article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows an Admin to add co-authors to an individual article

### S-3: allows an Admin to update the author

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows an Admin to update the author

### S-4: allows an Admin to mark an article as approved

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows an Admin to mark an article as approved

### S-5: allows an Admin to mark an article as featured

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows an Admin to mark an article as featured

### S-6: allows an Admin to mark an article as pinned

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows an Admin to mark an article as pinned

### S-7: allows an Admin to update the published at datetime for an article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows an Admin to update the published at datetime for an article

### S-8: creates an audit log on update

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an audit log on update

### S-9: responds with :not_found with an invalid article id

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** responds with :not_found with an invalid article id

### S-10: allows an admin to unpin an article

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows an admin to unpin an article

### S-11: allows an admin to unpin an article via Ajax

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows an admin to unpin an article via Ajax

### S-12: creates an audit log

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates an audit log

