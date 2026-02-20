---
id: "01KHY7Q0T6K89CB4D6VP02NYDJ"
name: "ahoy_email_clicks_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/ahoy/email_clicks_controller.rb
- spec/requests/ahoy/email_clicks_spec.rb

## Functional Overview

This specification defines the expected behavior of `"AhoyEmailClicks"` within the emails domain.

### Behavioral Areas

- **AhoyEmailClicks**: Ensures correct behavior under the specified conditions
- **POST /email_clicks**: Ensures correct behavior under the specified conditions
- **with a valid signature**: records feed event if article with url path exists
- **with an invalid signature**: records feed event if article with url path exists

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/ahoy/email_clicks_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: publishes a click event and returns http ok

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** publishes a click event and returns http ok

### S-2: Records billboard event if params[:bb] present

- **Given** params[:bb] present
- **When** the action is triggered
- **Then** Records billboard event

### S-3: records feed event if article with url path exists

- **Given** article with url path exists
- **When** the action is triggered
- **Then** records feed event

### S-4: updates the user

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** updates the user

### S-5: returns http forbidden

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns http forbidden

