---
id: "01KHY7PZYNCPE3JBEE59JS9V3Z"
name: "re_captcha_check_registration_enabled_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/re_captcha/check_registration_enabled.rb
- spec/services/re_captcha/check_registration_enabled_spec.rb

## Functional Overview

This specification defines the expected behavior of `ReCaptcha::CheckRegistrationEnabled` within the users domain.

### Behavioral Areas

- **ReCaptcha for registration**: is disabled if recaptcha disabled for email signup
- **when recaptcha is enabled**: is enabled if both site & secret keys present

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/re_captcha/check_registration_enabled.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: is enabled if both site & secret keys present

- **Given** both site & secret keys present
- **When** the action is triggered
- **Then** is enabled

### S-2: is disabled if site or secret key missing

- **Given** site or secret key missing
- **When** the action is triggered
- **Then** is disabled

### S-3: is disabled if recaptcha disabled for email signup

- **Given** recaptcha disabled for email signup
- **When** the action is triggered
- **Then** is disabled

