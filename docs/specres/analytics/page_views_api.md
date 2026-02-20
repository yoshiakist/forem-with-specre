---
id: "01KHY7Q0Z6JB4P278GC6H36JRJ"
name: "page_views_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/page_views_controller.rb
- app/workers/articles/update_organic_page_views_worker.rb
- app/workers/articles/update_page_views_worker.rb
- spec/requests/page_views_spec.rb

## Functional Overview

This specification defines the expected behavior of `"PageViews"` within the analytics domain.

### Behavioral Areas

- **PageViews**: Ensures correct behavior under the specified conditions
- **POST /page_views**: Ensures correct behavior under the specified conditions
- **when user signed in**: sends user agent
- **when part of field test**: converts field test
- **when not part of field test**: converts field test
- **when user not signed in**: sends user agent
- **PUT /page_views/:id**: Ensures correct behavior under the specified conditions
- **when user is signed in**: sends user agent

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/page_views_controller.rb` -- HTTP request routing and response handling
- **Background worker**: `app/workers/articles/update_organic_page_views_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/articles/update_page_views_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: creates a new page view

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new page view

### S-2: sends referrer

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends referrer

### S-3: sends user agent

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends user agent

### S-4: sends Algolia insight event

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends Algolia insight event

### S-5: Does not send an Algolia event if Algolia setting not present

- **Given** Algolia setting not present
- **When** the action is triggered
- **Then** Does not send an Algolia event

### S-6: converts field test

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** converts field test

### S-7: does not convert field test

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not convert field test

### S-8: creates a new page view

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates a new page view

### S-9: stores aggregate page views

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** stores aggregate page views

### S-10: stores aggregate organic page views

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** stores aggregate organic page views

### S-11: sends referrer

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends referrer

### S-12: sends user agent

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** sends user agent

