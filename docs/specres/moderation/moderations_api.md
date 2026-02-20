---
id: "01KHY7Q0MZQV8NAXFR42RKJZT8"
name: "moderations_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/moderations_controller.rb
- spec/requests/moderations_spec.rb

## Functional Overview

This specification defines the expected behavior of `"Moderations"` within the moderation domain.

### Behavioral Areas

- **when not logged-in**: renders not_found when an article can
- **when user is not trusted**: renders not_found when an article can
- **Moderations**: Ensures correct behavior under the specified conditions
- **when user is trusted**: renders not_found when an article can
- **actions_panel**: Ensures correct behavior under the specified conditions
- **when the user is a tag moderator**: renders not_found when an article can
- **when the user is trusted**: renders not_found when an article can
- **when the user is an admin**: renders not_found when an article can

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/moderations_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: does not grant access

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not grant access

### S-2: raises Pundit::NotAuthorizedError internally

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** raises Pundit::NotAuthorizedError internally

### S-3: does not grant access

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not grant access

### S-4: internally raise Pundit::NotAuthorized internally

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** internally raise Pundit::NotAuthorized internally

### S-5: grants access to comment moderation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** grants access to comment moderation

### S-6: grant access to article moderation

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** grant access to article moderation

### S-7: grants access to /mod index

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** grants access to /mod index

### S-8: grants access to /mod index with articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** grants access to /mod index with articles

### S-9: grants access to /mod/:tag index with articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** grants access to /mod/:tag index with articles

### S-10: returns not found for inappropriate tags

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns not found for inappropriate tags

### S-11: only includes articles which do not have [Boost] in as title

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** only includes articles which do not have [Boost] in as title

### S-12: renders not_found when an article can

- **Given** the system is in a standard operational state
- **When** an article can
- **Then** renders not_found

