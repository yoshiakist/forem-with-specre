---
id: "01KHY7PZSFKPSJDKPY51PJGA3J"
name: "user_decorator_decorator"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/decorators/user_decorator.rb
- spec/decorators/user_decorator_spec.rb

## Functional Overview

This specification defines the expected behavior of `UserDecorator` within the users domain.

### Behavioral Areas

- **with serialization**: creates proper body class with defaults
- **cached_followed_tags**: Ensures correct behavior under the specified conditions
- **darker_color**: Ensures correct behavior under the specified conditions
- **enriched_colors**: Ensures correct behavior under the specified conditions
- **config_body_class**: Ensures correct behavior under the specified conditions
- **when user with roles**: returns array of tags if user follows them
- **fully_banished?**: Ensures correct behavior under the specified conditions
- **considered_new?**: delegates to Settings::RateLimit.considered_new?

### Implementation Architecture

The behavior is implemented across the following layers:

- **Decorator**: `app/decorators/user_decorator.rb` -- presentation logic and view-model enrichment


## Scenarios

### S-1: serializes both the decorated object IDs and decorated methods

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** serializes both the decorated object IDs and decorated methods

### S-2: serializes collections of decorated objects

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** serializes collections of decorated objects

### S-3: returns array of tags if user follows them

- **Given** user follows them
- **When** the action is triggered
- **Then** returns array of tags

### S-4: returns a darker version of the assigned color if colors are blank

- **Given** colors are blank
- **When** the action is triggered
- **Then** returns a darker version of the assigned color

### S-5: returns a darker version of the color if brand_color1 is present

- **Given** brand_color1 is present
- **When** the action is triggered
- **Then** returns a darker version of the color

### S-6: returns an adjusted darker version of the color

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** returns an adjusted darker version of the color

### S-7: returns an adjusted lighter version of the color if adjustment is over 1.0

- **Given** adjustment is over 1.0
- **When** the action is triggered
- **Then** returns an adjusted lighter version of the color

### S-8: returns assigned colors if brand_color1 is blank

- **Given** brand_color1 is blank
- **When** the action is triggered
- **Then** returns assigned colors

### S-9: returns brand_color1 if present

- **Given** present
- **When** the action is triggered
- **Then** returns brand_color1

### S-10: creates proper body class with defaults

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates proper body class with defaults

### S-11: includes user role names in body class

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** includes user role names in body class

### S-12: creates proper body class with sans serif config

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** creates proper body class with sans serif config

