---
id: "01KHYCM33CMWM4X1249Z9032CQ"
name: "system_retags_aliased_content"
status: "draft"
---

## Related Files

- app/workers/tags/alias_retag_worker.rb

## Functional Overview

`Tags::AliasRetagWorker` is a Sidekiq background job that bulk-updates all content tagged with a given tag after an alias relationship is established. It iterates through every tagging record for the tag, re-parses the taggable object's tag list (which resolves aliases to preferred tags), and saves the updated list. This ensures historical content is retroactively retagged when tags are consolidated.

## Scenarios

### System retags all content for an aliased tag

1. When a tag's `alias_for` is set, the admin controller enqueues `Tags::AliasRetagWorker` with the tag ID.
2. The worker looks up the tag; if it no longer exists, it exits silently.
3. For each tagging associated with the tag, the worker loads the taggable object (e.g., Article).
4. The worker re-parses the taggable's current tag list through `ActsAsTaggableOn::TagParser`, which resolves alias names to preferred tag names.
5. The taggable is saved with the updated tag list, effectively replacing the aliased tag with the preferred tag.
6. Taggings whose taggable no longer exists are silently skipped.

## Design Intent

The worker runs on the `low_priority` queue with a concurrency limit of 1 and 5 retries. This throttling prevents database contention when retagging large volumes of content. The use of `find_each` ensures memory-efficient batch processing.
