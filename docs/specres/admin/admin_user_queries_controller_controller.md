---
id: "01KHY7Q0ZPGYP5XHTQ1R20TSJS"
name: "admin_user_queries_controller_controller"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files


- spec/controllers/admin/user_queries_controller_spec.rb

## Functional Overview

This specification defines the expected behavior of `Admin::UserQueriesController` within the admin domain.

### Behavioral Areas

- **GET #index**: Ensures correct behavior under the specified conditions
- **GET #show**: Ensures correct behavior under the specified conditions
- **GET #new**: Ensures correct behavior under the specified conditions
- **POST #create**: Ensures correct behavior under the specified conditions
- **with valid parameters**: validates a query and returns JSON
- **with invalid parameters**: returns validation errors for invalid queries
- **GET #edit**: Ensures correct behavior under the specified conditions
- **PATCH #update**: Ensures correct behavior under the specified conditions


## Scenarios

### S-1: returns a successful response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a successful response

### S-2: assigns user queries

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns user queries

### S-3: filters by active status

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters by active status

### S-4: searches by name or description

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** searches by name or description

### S-5: returns a successful response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a successful response

### S-6: assigns the user query

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns the user query

### S-7: calculates estimated count

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** calculates estimated count

### S-8: returns a successful response

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns a successful response

### S-9: assigns a new user query

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns a new user query

### S-10: creates a new user query

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new user query

### S-11: assigns the created user query to current user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** assigns the created user query to current user

### S-12: redirects to the created user query

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** redirects to the created user query

