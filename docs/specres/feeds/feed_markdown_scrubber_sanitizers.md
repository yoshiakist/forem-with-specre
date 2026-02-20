---
id: "01KHY7Q0Q9AMNPBPDKXW655C4D"
name: "feed_markdown_scrubber_sanitizers"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/sanitizers/feed_markdown_scrubber.rb
- spec/sanitizers/feed_markdown_scrubber_spec.rb

## Functional Overview

This specification defines the expected behavior of `FeedMarkdownScrubber` within the feeds domain.

### Implementation Architecture

The behavior is implemented across the following layers:

- `app/sanitizers/feed_markdown_scrubber.rb`


## Scenarios

### S-1: allows the tags specified by MarkdownProcessor

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows the tags specified by MarkdownProcessor

### S-2: scrubs out tags not allowed by MarkdownProcessor

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** scrubs out tags not allowed by MarkdownProcessor

### S-3: allows attributes allowed by MarkdownProcessor

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows attributes allowed by MarkdownProcessor

### S-4: scrubs out attributes not allowed by MarkdownProcessor

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** scrubs out attributes not allowed by MarkdownProcessor

### S-5: allows links in 

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** allows links in 

### S-6: scrubs relative links

- **Given** the preconditions are satisfied
- **When** the operation is executed
- **Then** scrubs relative links

### S-7: does not scrub anchors with no link

- **Given** the preconditions are satisfied
- **When** the operation is invoked
- **Then** the system does not scrub anchors with no link

