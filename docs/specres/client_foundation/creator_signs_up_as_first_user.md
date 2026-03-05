---
id: "01KJXXTGC5AP94N2XKXRW043X2"
name: "creator_signs_up_as_first_user"
status: "draft"
---

## Related Files

- `app/javascript/packs/foremCreatorSignup.js`

## Functional Overview

When an administrator sets up a new Forem instance, a dedicated creator signup page is presented. This page collects the creator's display name, email, and password. As the creator types their name, a sanitized username is automatically suggested and pre-filled, derived by lowercasing the name and replacing non-alphanumeric characters with underscores, truncated to 30 characters. The creator can either accept the suggested username or click an edit link to reveal the username input field and type a custom value. A password-visibility toggle on each password field lets the creator view or hide their password as they type.

## Design Intent

Auto-deriving a username from the display name reduces friction during the one-time creator setup flow, where there are no other users to conflict with. The suggestion is shown as a non-editable hint initially; the explicit "edit" action keeps the form uncluttered while still giving the creator full control. Password visibility toggling is provided as an accessibility and usability aid so the creator can confirm a complex password before submitting.

## Key Members

- `js-creator-signup-name` — input element for the creator's display name; drives automatic username suggestion
- `js-creator-signup-username` — hidden username input whose value is pre-filled with the derived hint
- `js-creator-signup-username-row` — wrapper row for the username input; hidden by default until "edit" is clicked
- `js-creator-signup-username-hint` — inline display element showing the auto-derived username hint
- `js-creator-signup-username-hint-row` — row containing the username hint; shown when the name field has a value and the username row is still hidden
- `js-creator-edit-username` — button or link that reveals the username field for custom entry
- `js-password-toggle-wrapper` — wrapper around each password field and its visibility toggle
- `js-password` — password input whose type alternates between `password` and `text`
- `js-creator-password-visibility` — toggle button that switches password visibility; tracks state with `aria-pressed`
- `js-eye` / `js-eye-off` — icon elements toggled to reflect the current password-visibility state

## Scenarios

### Creator types a display name and a username hint appears

1. The creator opens the signup page; the username input row and hint row are both hidden.
2. The creator types characters into the name field.
3. On each input event, the system derives a username hint by lowercasing the name, replacing every non-alphanumeric character with an underscore, and truncating the result to 30 characters.
4. The hint is displayed in the hint element and simultaneously written into the (still-hidden) username input field.
5. The hint row becomes visible below the name field.

### Creator accepts the suggested username

1. The creator leaves the username row hidden and proceeds to fill in the remaining form fields.
2. The username input already holds the most recently derived hint value.
3. The form submits with the auto-derived username.

### Creator chooses a custom username

1. The creator clicks the "edit username" link.
2. The username input row is revealed and the username field receives focus immediately (via a zero-delay timeout to allow the DOM to render).
3. The hint row is hidden.
4. The creator types a custom username; further changes to the name field no longer update the username input because the username row is no longer hidden.

### Creator toggles password visibility

1. The creator clicks the password-visibility button (eye icon) within a password wrapper.
2. The password field type switches from `password` to `text`, revealing the entered value.
3. The eye-off icon is shown and the eye icon is hidden; the button's `aria-pressed` attribute is set to `true`.
4. Clicking the button again reverses all changes, masking the password.

## Failures / Exceptions

- If the name field is empty, the derived hint is an empty string; the hint row is still shown and the username input is set to an empty string.
- If any expected DOM element is missing (e.g., `.js-creator-signup-name` not present), a JavaScript error will be thrown at page load because elements are accessed unconditionally.
