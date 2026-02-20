---
id: "01KHY7PZCDTD7MRBWPJ46ZTBBT"
name: "articles_helper_helper"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/helpers/articles_helper.rb
- spec/helpers/articles_helper_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles_Helper` within the articles domain.

### Behavioral Areas

- **.get_host_without_www**: Ensures correct behavior under the specified conditions
- **image_tag_or_inline_svg_tag**: Ensures correct behavior under the specified conditions
- **with a width and height**: can handle urls without schemes
- **with #internal_navigation? set to false**: can handle urls without schemes
- **with width and height arguments, and with #internal_navigation? set to false**: can handle urls without schemes
- **utc_iso_timestamp**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **View helper**: `app/helpers/articles_helper.rb` -- shared view utility methods


## Scenarios

### S-1: Data integrity and associations

The model enforces the following constraints:

- start with "<img"
- include 'width="18" height="18"'
- start with '<svg xmlns="http://www.w3.org/2000/svg"'
- include 'width="18" height="18"'

**Verification:** All constraints are enforced at the model level, preventing invalid data from being persisted to the database. Violations produce descriptive error messages on the model's `errors` collection.

### S-2: drops the www off of a valid url

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** drops the www off of a valid url

### S-3: lowercases the host name in general

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** lowercases the host name in general

### S-4: titlecases the host for medium.com and drops .com

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** titlecases the host for medium.com and drops .com

### S-5: can handle urls without schemes

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** can handle urls without schemes

### S-6: can handle URLs with leading and trailing whitespace

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** can handle URLs with leading and trailing whitespace

### S-7: correctly formats the date when present

- **Given** the system is in a standard operational state
- **When** present
- **Then** correctly formats the date

### S-8: returns nil if there is no timestamp

- **Given** there is no timestamp
- **When** the action is triggered
- **Then** returns nil

