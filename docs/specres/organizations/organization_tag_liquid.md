---
id: "01KHY7Q0H9DDBH49RXB5671TNG"
name: "organization_tag_liquid"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/liquid_tags/organization_tag.rb
- spec/liquid_tags/organization_tag_spec.rb

## Functional Overview

This specification defines the expected behavior of `OrganizationTag` within the organizations domain.

### Behavioral Areas

- **when given valid id_code**: rejects invalid id_code

### Implementation Architecture

The behavior is implemented across the following layers:

- **Liquid tag**: `app/liquid_tags/organization_tag.rb` -- custom Markdown/Liquid embed rendering


## Scenarios

### S-1: renders the proper user name

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders the proper user name

### S-2: renders image html

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** renders image html

### S-3: rejects invalid id_code

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** rejects invalid id_code

