---
id: "01KHZ6CQSTGFQY3V3VHN924EF9"
name: "user_can_moderate_from_profile_dropdown"
status: "draft"
---

## Related Files

- `app/javascript/packs/profileDropdown.js`
- `app/javascript/profileDropdown/blockButton.js`
- `app/javascript/profileDropdown/flagButton.js`
- `app/javascript/profileDropdown/spamButton.js`

## Functional Overview

When a logged-in user visits another user's profile page, the profile dropdown menu is initialized with moderation actions appropriate to the viewer's role. Any authenticated user can block or unblock the profile owner, which prevents the blocked user from commenting on the viewer's posts and hides their content from the viewer's feed. Trusted users and admins additionally see a flag button that toggles the profile owner's content visibility site-wide via a `vomit` reaction. Admins see a spam button that can assign or remove the spam role, hiding or restoring all of the target user's posts and comments. The dropdown is initialized only once per page load, the current user's own profile hides the entire dropdown, and each action button is hidden from users who lack the required role or who are viewing their own profile.

## Design Intent

Each moderation action is scoped to the minimum required role: blocking is available to all authenticated users, flagging to trusted users and admins, and spam marking exclusively to admins. This layered approach lets community members protect themselves while reserving heavier moderation tools for privileged roles. Actions that a user cannot perform are removed from the DOM entirely rather than merely disabled, reducing confusion and surface area for abuse.

## Key Members

- `profileDropdownDiv.dataset.dropdownInitialized` — guards against re-initializing the dropdown on the same page load
- `blockButton.dataset.profileUserId` — the numeric ID of the profile owner, used as the target for block/unblock API calls
- `flagButton.dataset.isUserFlagged` — boolean string indicating the current flag state, toggled locally after a successful API response
- `spamButton.dataset.isUserSpam` — boolean string indicating whether the spam role is currently applied, toggled locally after a successful API response
- `user.trusted`, `user.admin` — role fields on the current user object that gate visibility of the flag and spam buttons respectively

## Scenarios

### Dropdown initialization on another user's profile

1. The page loads and `initDropdown` is called.
2. The `.profile-dropdown` element is found; if it has already been initialized, execution stops.
3. The current user's identity is retrieved via `userData()`.
4. If the current user's username matches the profile owner's username, the dropdown is hidden and no further setup occurs.
5. The dropdown trigger (`user-profile-dropdown`) and menu (`user-profile-dropdownmenu`) are registered with `initializeDropdown`.
6. The "Report Abuse" link is injected as a real anchor using the path stored in `data-path`.
7. `initBlock`, `initFlag`, and `initSpam` are called to attach moderation behavior, and the dropdown is marked as initialized.

### Any authenticated user blocks the profile owner

1. The block button (`user-profile-dropdownmenu-block-button`) is present and the viewer is not the profile owner.
2. On load, the system checks `GET /user_blocks/:id`; if the result is `blocking`, the button label becomes "Unblock" and the unblock handler is attached; otherwise the block handler is attached.
3. The user clicks the button; a confirmation dialog explains the consequences of blocking.
4. On confirmation, `POST /user_blocks` is called with `blocked_id`.
5. If the response result is `blocked`, the button label changes to "Unblock" and the unblock handler is registered for the next click.

### Any authenticated user unblocks the profile owner

1. The block button label is "Unblock" and the unblock handler is active.
2. The user clicks the button; `DELETE /user_blocks/:id` is called with `blocked_id`.
3. If the response result is `unblocked`, the button label reverts to "Block" and the block handler is registered for the next click.

### Trusted user or admin flags the profile owner

1. The flag button (`user-profile-dropdownmenu-flag-button`) is present.
2. After resolving user data, if the viewer is neither trusted nor admin, or is viewing their own profile, the button is removed from the DOM.
3. A qualifying viewer clicks the button; a confirmation dialog describes the visibility impact.
4. On confirmation, `POST /reactions` is called with `reactable_type: 'User'`, `category: 'vomit'`, and `reactable_id`.
5. If the response result is `create`, `isUserFlagged` is set to `true` and the button label changes to `Unflag <username>`; otherwise the flag is toggled off and the label reverts to `Flag <username>`.

### Admin marks the profile owner as spam or restores good standing

1. The spam button (`user-profile-dropdownmenu-spam-button`) is present.
2. After resolving user data, if the viewer is not an admin, the button is removed from the DOM.
3. An admin clicks the button; a confirmation dialog describes the consequences of applying or removing the spam role.
4. On confirmation, `PUT /users/:id/spam` is called to add the spam role, or `DELETE /users/:id/spam` to remove it.
5. If the response is successful, `isUserSpam` is toggled and the button label updates accordingly.

## Failures / Exceptions

- If the block, flag, or spam API call fails (network error or unhandled status), an `alert` is shown with the error message and the button state is not changed.
- A `422` response from the block/unblock endpoint surfaces the server-provided `error` message in an alert.
- Flag and spam failures are additionally reported to `Honeybadger` with a descriptive message and the target user ID.
- If the viewer is unauthenticated (`userData()` returns falsy), the block button setup exits early and the flag and spam buttons are removed from the DOM.
