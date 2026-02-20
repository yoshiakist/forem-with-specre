---
id: "01KHY7PZCABZR4K92TKZ92NM11"
name: "article_decorator_decorator"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/decorators/article_decorator.rb
- spec/decorators/article_decorator_spec.rb

## Functional Overview

This specification defines the expected behavior of `ArticleDecorator` within the articles domain.

### Behavioral Areas

- **with serialization**: returns the article url without a canonical_url
- **user_data_info_to_json**: Ensures correct behavior under the specified conditions
- **current_state_path**: Ensures correct behavior under the specified conditions
- **has_recent_comment_activity?**: Ensures correct behavior under the specified conditions
- **processed_canonical_url**: Ensures correct behavior under the specified conditions
- **cached_tag_list_array**: Ensures correct behavior under the specified conditions
- **url**: Ensures correct behavior under the specified conditions
- **title_length_classification**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Decorator**: `app/decorators/article_decorator.rb` -- presentation logic and view-model enrichment


## Scenarios

### S-1: serializes both the decorated object IDs and decorated methods

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** serializes both the decorated object IDs and decorated methods

### S-2: serializes collections of decorated objects

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** serializes collections of decorated objects

### S-3: returns an escaped JSON string

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an escaped JSON string

### S-4: returns the path /:username/:slug when published

- **Given** the system is in a standard operational state
- **When** published
- **Then** returns the path /:username/:slug

### S-5: returns the path /:username/:slug?:password when draft

- **Given** the system is in a standard operational state
- **When** draft
- **Then** returns the path /:username/:slug?:password

### S-6: returns the path /:username/:slug?:password when scheduled

- **Given** the system is in a standard operational state
- **When** scheduled
- **Then** returns the path /:username/:slug?:password

### S-7: returns false if no comment activity

- **Given** no comment activity
- **When** the action is triggered
- **Then** returns false

### S-8: returns true if more recent than passed in value

- **Given** more recent than passed in value
- **When** the action is triggered
- **Then** returns true

### S-9: returns false if less recent than passed in value

- **Given** less recent than passed in value
- **When** the action is triggered
- **Then** returns false

### S-10: strips canonical_url

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** strips canonical_url

### S-11: returns the article url without a canonical_url

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the article url without a canonical_url

### S-12: returns no tags if the cached tag list is empty

- **Given** the cached tag list is empty
- **When** the action is triggered
- **Then** returns no tags

