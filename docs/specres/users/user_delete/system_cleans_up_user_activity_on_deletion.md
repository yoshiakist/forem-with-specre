---
id: "01KJBEE5MYMJHSJMTMR3XN0BAT"
name: "system_cleans_up_user_activity_on_deletion"
status: "draft"
---

## Related Files

- `app/services/users/delete_activity.rb`
- `spec/services/users/delete_spec.rb` (Test)

## Functional Overview

When a user account is being deleted, the system removes or nullifies all activity and profile data associated with that user. This includes social media connections (GitHub repositories), profile information (notifications, reactions, follows, mentions, badge achievements, collections, credits, organization memberships, profile pins, and social username fields), as well as API secrets, podcasts created by the user, block relationships, authored notes, billboard events, email messages, HTML variants, poll interactions, response templates, and listings. Feedback messages are handled with nuance: messages where the user was the offender are marked as "Resolved" rather than deleted, while messages where the user was the reporter or affected party are deleted outright. The module is designed to be called by a higher-level orchestrator as a discrete cleanup step.

## Design Intent

The module separates cleanup concerns into focused sub-routines (`delete_social_media`, `delete_profile_info`, `delete_feedback_messages`) to improve readability and allow independent reasoning about each category of data. The decision to use `delete_all` (bypassing callbacks) rather than `destroy_all` for most associations prioritizes performance; `destroy_all` is used only for listings, where callbacks or dependent-destroy logic are needed. Offender feedback messages are resolved rather than deleted to preserve audit history, reflecting a policy that accountability records should survive account removal.

## Scenarios

### Cleaning up social media connections

1. The system is called with the user being deleted.
2. All GitHub repository records associated with the user are removed directly from the database without triggering model callbacks.

### Cleaning up profile information

1. The system removes all notifications, reactions, reactions directed at the user, follows, mentions, badge achievements, collections, credits, organization memberships, and profile pins.
2. Any follows where the user is the followable target are also removed.
3. The user's profile summary, location, website URL, and extra data fields are cleared to empty values.
4. The user's linked social usernames (GitHub, Twitter, Facebook) are set to empty strings and the record is saved.

### Cleaning up activity records

1. The system removes all API secrets belonging to the user.
2. Podcasts the user created have their creator reference nullified (set to nil) rather than being deleted.
3. All block relationships where the user is the blocker or the blocked party are removed.
4. Authored notes, billboard events, email messages, HTML variants, poll skips, poll votes, and response templates are all removed.
5. Listings belonging to the user are destroyed (with callbacks).

### Handling feedback messages on deletion

1. Feedback messages where the user was identified as the offender are updated to a status of "Resolved" rather than deleted.
2. Feedback messages where the user was the reporter are deleted.
3. Feedback messages where the user was the affected party are deleted.

## Failures / Exceptions

- No explicit error handling is present in the module; failures in any step will propagate as unhandled exceptions to the calling orchestrator.
