---
id: "01KHY7PZNY1BFXQFWE6JTCBDZ4"
name: "comment_decorator_decorator"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/decorators/comment_decorator.rb
- spec/decorators/comment_decorator_spec.rb

## Functional Overview

This specification defines the expected behavior of `CommentDecorator` within the comments domain.

### Behavioral Areas

- **with serialization**: Ensures correct behavior under the specified conditions
- **low_quality**: Ensures correct behavior under the specified conditions
- **published_timestamp**: Ensures correct behavior under the specified conditions
- **published_at_int**: Ensures correct behavior under the specified conditions

### Implementation Architecture

The behavior is implemented across the following layers:

- **Decorator**: `app/decorators/comment_decorator.rb` -- presentation logic and view-model enrichment


## Scenarios

### S-1: serializes both the decorated object IDs and decorated methods

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** serializes both the decorated object IDs and decorated methods

### S-2: serializes collections of decorated objects

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** serializes collections of decorated objects

### S-3: returns true if the comment is low quality

- **Given** the comment is low quality
- **When** the action is triggered
- **Then** returns true

### S-4: returns false if the comment score is on threshold quality

- **Given** the comment score is on threshold quality
- **When** the action is triggered
- **Then** returns false

### S-5: returns false if the comment is a good quality

- **Given** the comment is a good quality
- **When** the action is triggered
- **Then** returns false

### S-6: returns empty string if the comment is new

- **Given** the comment is new
- **When** the action is triggered
- **Then** returns empty string

### S-7: returns the timestamp of the creation date

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the timestamp of the creation date

### S-8: returns the creation date as an integer

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns the creation date as an integer

