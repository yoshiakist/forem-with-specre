---
id: "01KJBEAAQ5B160HFTWKSHPA73N"
name: "system_represents_deleted_user_as_null_object"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/models/users/deleted_user.rb`
- `spec/models/users/deleted_user_spec.rb` (Test)

## Functional Overview

The system represents a deleted user through the `Users::DeletedUser` module, which implements the Null Object pattern. Rather than scattering nil-guards throughout the codebase when a referenced user no longer exists, callers receive a module singleton that responds to the same interface as a live user. It returns safe, meaningful defaults for all display-related attributes — including a fixed username of "[deleted user]", a translated display name, predefined background and foreground colors for rendering, and nil for any personally identifiable or profile-specific fields. The module also exposes `deleted?` returning `true` and `class_name` returning `User.name`, enabling consuming code to treat it polymorphically with real `User` records without raising `NoMethodError`.

## Design Intent

Deleted user data must not be retained, yet the rest of the application still needs to render content that was authored by or associated with a now-deleted account (e.g., tags, rich content embeds). The Null Object approach avoids conditional branching at every call site and keeps the rendering pipeline uniform. The module acts as `self` rather than an instance so no allocation is required and its identity is stable across the application lifecycle.

## Key Members

- `BG_COLOR` / `FG_COLOR` — fixed hex color strings used for avatar and badge rendering when no real profile colors are available.
- `ENRICHED_COLORS` — hash combining the two colors under `:bg` and `:text` keys, returned by `enriched_colors`.
- `USER_COLORS` — array of the two color strings passed to `Color::CompareHex` for brightness calculation via `darker_color`.

## Scenarios

### System encounters a deleted user reference during rendering

1. Code that would normally call methods on a `User` record receives `Users::DeletedUser` instead.
2. It calls display attributes such as `username`, `name`, `path`, `profile_image_url`, or `tag_line`.
3. `Users::DeletedUser` returns the safe default for each: `"[deleted user]"` for `username`, the I18n-translated string for `name`, and `nil` for any personal or link attributes.
4. The rendering pipeline completes without errors or nil-related exceptions.

### System checks whether a user reference is deleted

1. Code calls `deleted?` on the object it holds.
2. `Users::DeletedUser` returns `true`, allowing the caller to branch or display a tombstone state if desired.

### System uses deleted user colors for avatar or badge rendering

1. Code calls `enriched_colors` to obtain the color hash.
2. `Users::DeletedUser` returns `{ bg: "#19063A", text: "#DCE9F3" }`.
3. Code calls `darker_color` to determine the dominant shade; `Users::DeletedUser` computes brightness via `Color::CompareHex` over the two fixed colors and returns the result.

### System requests a sized profile image URL for a deleted user

1. Code calls `profile_image_url_for(length: <size>)` on the deleted user object.
2. `Users::DeletedUser` passes `nil` (its `profile_image_url`) and the requested length to `Images::Profile.call`.
3. The image helper returns a placeholder or default image URL appropriate for the given size.

### System decorates the deleted user object

1. Code calls `decorate` on the object, expecting a decorated user.
2. `Users::DeletedUser.decorate` returns `self`, so the module itself acts as its own decorator and no additional wrapping is performed.
