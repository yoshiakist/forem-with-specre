---
id: "01KHY7Q1GP6SDGJ4DNCDNR17Y0"
name: "forem_instance_model"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/models/forem_instance.rb
- app/models/creator_setting.rb
- spec/models/forem_instance_spec.rb

## Functional Overview

This specification defines the expected behavior of `ForemInstance` within the settings domain.

### Behavioral Areas

- **deployed_at**: Ensures correct behavior under the specified conditions
- **latest_commit_id**: Ensures correct behavior under the specified conditions
- **.local?**: Ensures correct behavior under the specified conditions
- **.dev_to?**: Ensures correct behavior under the specified conditions
- **.smtp_enabled?**: Ensures correct behavior under the specified conditions
- **.contact_email**: Ensures correct behavior under the specified conditions
- **.reply_to_email_address**: Ensures correct behavior under the specified conditions
- **when the minimum SMTP settings have been provided**: return false when no credential is provided

### Implementation Architecture

The behavior is implemented across the following layers:

- **Model layer**: `app/models/forem_instance.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/creator_setting.rb` -- data persistence, validations, and associations


## Scenarios

### S-1: sets the RELEASE_FOOTPRINT if present

- **Given** present
- **When** the action is triggered
- **Then** sets the RELEASE_FOOTPRINT

### S-2: sets the HEROKU_RELEASE_CREATED_AT if the RELEASE_FOOTPRINT is not present

- **Given** the RELEASE_FOOTPRINT is not present
- **When** the action is triggered
- **Then** sets the HEROKU_RELEASE_CREATED_AT

### S-3: sets to current time if HEROKU_RELEASE_CREATED_AT and RELEASE_FOOTPRINT are not ...

- **Given** HEROKU_RELEASE_CREATED_AT and RELEASE_FOOTPRINT are not present
- **When** the action is triggered
- **Then** sets to current time

### S-4: sets the FOREM_BUILD_SHA if present

- **Given** present
- **When** the action is triggered
- **Then** sets the FOREM_BUILD_SHA

### S-5: sets the HEROKU_RELEASE_CREATED_AT if the RELEASE_FOOTPRINT is not present

- **Given** the RELEASE_FOOTPRINT is not present
- **When** the action is triggered
- **Then** sets the HEROKU_RELEASE_CREATED_AT

### S-6: returns true if the .app_domain points to localhost

- **Given** the .app_domain points to localhost
- **When** the action is triggered
- **Then** returns true

### S-7: returns false if the .app_domain points to a regular domain

- **Given** the .app_domain points to a regular domain
- **When** the action is triggered
- **Then** returns false

### S-8: returns true if the .app_domain is dev.to

- **Given** the .app_domain is dev.to
- **When** the action is triggered
- **Then** returns true

### S-9: returns false if the .app_domain is not dev.to

- **Given** the .app_domain is not dev.to
- **When** the action is triggered
- **Then** returns false

### S-10: return false when no credential is provided

- **Given** the system is in a standard operational state
- **When** no credential is provided
- **Then** return false

### S-11: returns true if provided_minimum_settings?

- **Given** provided_minimum_settings?
- **When** the action is triggered
- **Then** returns true

### S-12: returns true if sendgrid api key is available

- **Given** sendgrid api key is available
- **When** the action is triggered
- **Then** returns true

