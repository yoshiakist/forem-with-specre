---
id: "01KHY7Q0ZYTV8P70KHT2AQHDDT"
name: "admin_gdpr_delete_requests_query_query"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/queries/admin/gdpr_delete_requests_query_spec.rb

## Functional Overview

This specification defines the expected behavior of `Admin::GDPRDeleteRequestsQuery` within the admin domain.

### Behavioral Areas

- **.call**: Ensures correct behavior under the specified conditions
- **when no arguments are given**: Ensures correct behavior under the specified conditions
- **when searching for a user by username**: returns all users
- **when searching for a user by email**: returns all users
- **when searching for ambiguous terms that matches multiple users**: returns all users
- **when searching for ambiguous terms that matches both emails and usernames**: Ensures correct behavior under the specified conditions
- **when passed a non-existent email or username**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- match array [gdpr delete request 2]
- match array [gdpr delete request 1]
- match array [gdpr delete request 1, gdpr delete request 11]
- match array [gdpr delete request 1, gdpr delete request 2, gdpr delete request 3, gdpr delete request 11]
- match array []

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: returns all users

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns all users

