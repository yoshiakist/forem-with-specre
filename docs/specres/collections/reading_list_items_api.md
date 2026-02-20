---
id: "01KHY7Q1CCPDNMCQJ5PAFAPXSY"
name: "reading_list_items_api"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/controllers/reading_list_items_controller.rb
- spec/requests/reading_list_items_spec.rb

## Functional Overview

This specification defines the expected behavior of `"ReadingListItems"` within the collections domain.

### Behavioral Areas

- **ReadingListItems**: Ensures correct behavior under the specified conditions
- **GET reading list**: returns reading list page
- **PUT reading_list_items/:id**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Controller layer**: `app/controllers/reading_list_items_controller.rb` -- HTTP request routing and response handling


## Scenarios

### S-1: returns reading list page

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns reading list page

### S-2: returns archives item if no param

- **Given** no param
- **When** the action is triggered
- **Then** returns archives item

### S-3: unarchives an item if current_status is passed as archived

- **Given** current_status is passed as archived
- **When** the action is triggered
- **Then** unarchives an item

### S-4: raises NotAuthorizedError if current_user is not the reaction user

- **Given** current_user is not the reaction user
- **When** the action is triggered
- **Then** raises NotAuthorizedError

