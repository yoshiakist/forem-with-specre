---
id: "01KHY7Q0XD1F4N8D1VAA07Y1R5"
name: "billboards_filtered_ads_query_query"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/queries/billboards/filtered_ads_query.rb
- app/controllers/admin/billboards_controller.rb
- app/controllers/api/v1/billboards_controller.rb
- app/controllers/billboards_controller.rb
- app/workers/billboards/data_update_worker.rb
- app/workers/billboards/track_email_click_worker.rb
- spec/queries/billboards/filtered_ads_query_spec.rb

## Functional Overview

This specification defines the expected behavior of `Billboards::FilteredAdsQuery` within the billboards domain.

### Behavioral Areas

- **when ads are not approved or published**: does not display unapproved or unpublished ads
- **when considering article_tags**: suppresses external ads when permit_adjacent_sponsors is false
- **when available ads have matching tags**: shows no-tag billboards if the article tags do not contain matching tags
- **when considering user_tags**: suppresses external ads when permit_adjacent_sponsors is false
- **when available ads have matching tags**: shows no-tag billboards if the article tags do not contain matching tags
- **when considering users_signed_in**: suppresses external ads when permit_adjacent_sponsors is false
- **when considering article_exclude_ids**: suppresses external ads when permit_adjacent_sponsors is false
- **when considering audience segmentation**: suppresses external ads when permit_adjacent_sponsors is false

### Implementation Architecture

The behavior is implemented across the following layers:

- **Query object**: `app/queries/billboards/filtered_ads_query.rb` -- complex database query encapsulation
- **Controller layer**: `app/controllers/admin/billboards_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/api/v1/billboards_controller.rb` -- HTTP request routing and response handling
- **Controller layer**: `app/controllers/billboards_controller.rb` -- HTTP request routing and response handling
- **Background worker**: `app/workers/billboards/data_update_worker.rb` -- asynchronous job processing
- **Background worker**: `app/workers/billboards/track_email_click_worker.rb` -- asynchronous job processing


## Scenarios

### S-1: does not display unapproved or unpublished ads

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not display unapproved or unpublished ads

### S-2: shows no-tag billboards if the article tags do not contain matching tags

- **Given** the article tags do not contain matching tags
- **When** the action is triggered
- **Then** shows no-tag billboards

### S-3: shows billboards with no tags set if there are no article tags

- **Given** there are no article tags
- **When** the action is triggered
- **Then** shows billboards with no tags set

### S-4: shows the billboards that contain tags that match any of the article tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the billboards that contain tags that match any of the article tags

### S-5: shows no-tag billboards if the user tags do not contain matching tags

- **Given** the user tags do not contain matching tags
- **When** the action is triggered
- **Then** shows no-tag billboards

### S-6: shows billboards with no tags set if there are no user tags

- **Given** there are no user tags
- **When** the action is triggered
- **Then** shows billboards with no tags set

### S-7: shows the billboards that contain tags that match any of the user tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows the billboards that contain tags that match any of the user tags

### S-8: always shows :all, only shows -in/-out appropriately

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** always shows :all, only shows -in/-out appropriately

### S-9: shows billboards that exclude articles appropriately

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** shows billboards that exclude articles appropriately

### S-10: targets users in/out of segment appropriately

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** targets users in/out of segment appropriately

### S-11: shows page billboard if page is passed

- **Given** page is passed
- **When** the action is triggered
- **Then** shows page billboard

### S-12: always shows :community ad if matching, otherwise shows in_house/external

- **Given** matching, otherwise shows in_house/external
- **When** the action is triggered
- **Then** always shows :community ad

