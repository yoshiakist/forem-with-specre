---
id: "01KHY7PZH2AK2PKJH9JGQG8GKJ"
name: "articles_feeds_custom_service"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/articles/feeds/custom.rb
- app/models/articles/feeds.rb
- app/models/articles/feeds/lever_catalog_builder.rb
- app/models/articles/feeds/order_by_lever.rb
- app/models/articles/feeds/relevancy_lever.rb
- app/models/articles/feeds/variant_assembler.rb
- app/services/articles/feeds/article_score_calculator_for_user.rb
- app/services/articles/feeds/basic.rb
- app/services/articles/feeds/find_featured_story.rb
- app/services/articles/feeds/large_forem_experimental.rb
- app/services/articles/feeds/latest.rb
- spec/services/articles/feeds/custom_spec.rb

## Functional Overview

This specification defines the expected behavior of `Articles::Feeds::Custom` within the articles domain.

### Behavioral Areas

- **default_home_feed**: aliases feed to default_home_feed
- **when feed_config or user is nil**: returns an empty array if feed_config is nil
- **when valid feed_config and user are provided**: returns an empty array if feed_config is nil
- **when user has antifollowed tags**: returns an empty array if user is nil
- **when all articles are recent (within a week)**: returns only articles published after TIME_AGO_MAX sorted by computed score descending
- **dynamic shuffle count based on recent page views**: randomly shuffles the top 5 articles while keeping the rest in order
- **when recent_page_views_shuffle_weight is 0**: does not shuffle when not all articles are recent
- **when user has no recent page views**: returns an empty array if user is nil

### Implementation Architecture

The behavior is implemented across the following layers:

- **Service layer**: `app/services/articles/feeds/custom.rb` -- business logic orchestration and domain operations
- **Model layer**: `app/models/articles/feeds.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/lever_catalog_builder.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/order_by_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/relevancy_lever.rb` -- data persistence, validations, and associations
- **Model layer**: `app/models/articles/feeds/variant_assembler.rb` -- data persistence, validations, and associations
- **Service layer**: `app/services/articles/feeds/article_score_calculator_for_user.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/basic.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/find_featured_story.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/large_forem_experimental.rb` -- business logic orchestration and domain operations
- **Service layer**: `app/services/articles/feeds/latest.rb` -- business logic orchestration and domain operations


## Scenarios

### S-1: returns an empty array if feed_config is nil

- **Given** feed_config is nil
- **When** the action is triggered
- **Then** returns an empty array

### S-2: returns an empty array if user is nil

- **Given** user is nil
- **When** the action is triggered
- **Then** returns an empty array

### S-3: returns only articles published after TIME_AGO_MAX sorted by computed score desc...

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns only articles published after TIME_AGO_MAX sorted by computed score descending

### S-4: limits returns older article if lookback is configured very long

- **Given** lookback is configured very long
- **When** the action is triggered
- **Then** limits returns older article

### S-5: returns only very new articles if lookback is configured very short

- **Given** lookback is configured very short
- **When** the action is triggered
- **Then** returns only very new articles

### S-6: applies pagination via limit and offset

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** applies pagination via limit and offset

### S-7: filters out blocked articles

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** filters out blocked articles

### S-8: excludes articles tagged with antifollowed tags

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** excludes articles tagged with antifollowed tags

### S-9: randomly shuffles the top 5 articles while keeping the rest in order

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** randomly shuffles the top 5 articles while keeping the rest in order

### S-10: does not shuffle when not all articles are recent

- **Given** the system is in a standard operational state
- **When** not all articles are recent
- **Then** does not shuffle

### S-11: handles feeds with fewer than 5 articles correctly

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** handles feeds with fewer than 5 articles correctly

### S-12: uses default shuffle behavior (top 5) regardless of page view recency

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** uses default shuffle behavior (top 5) regardless of page view recency

