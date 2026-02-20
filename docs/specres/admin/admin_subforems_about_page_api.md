---
id: "01KHY7Q13AHA2SC3GPQ920WG44"
name: "admin_subforems_about_page_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/requests/admin/subforems_about_page_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Admin` within the admin domain.

### Behavioral Areas

- **Admin Subforems About Page Generation**: queues the worker with all parameters including name for about page generation
- **POST /admin/subforems with create_from_scratch parameters**: queues the worker with all parameters including name for about page generation
- **About page generation in worker**: queues the worker with all parameters including name for about page generation


## Scenarios

### S-1: queues the worker with all parameters including name for about page generation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** queues the worker with all parameters including name for about page generation

### S-2: generates an about page when worker runs

- **Given** the system is in a standard operational state
- **When** worker runs
- **Then** generates an about page

