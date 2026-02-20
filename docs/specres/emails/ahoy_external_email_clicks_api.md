---
id: "01KHY7Q0T8R5ZEK0AAVWW51Z3M"
name: "ahoy_external_email_clicks_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/ahoy/email_clicks_controller.rb
- spec/requests/ahoy/external_email_clicks_spec.rb

## Functional Overview

This specification defines the expected behavior of `"ExternalAhoyEmailClicks"` within the emails domain.

### Behavioral Areas

- **ExternalAhoyEmailClicks**: Ensures correct behavior under the specified conditions
- **GET #click**: Ensures correct behavior under the specified conditions
- **when bb parameter is present in the URL**: Ensures correct behavior under the specified conditions
- **when bb parameter is not present in the URL**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/ahoy/email_clicks_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: enqueues Billboards::TrackEmailClickWorker with bb and current_user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** enqueues Billboards::TrackEmailClickWorker with bb and current_user

### S-2: does not enqueue Billboards::TrackEmailClickWorker

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not enqueue Billboards::TrackEmailClickWorker

