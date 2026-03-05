---
id: "01KJXXHMXT7M0M6E0BCSN0PA34"
name: "system_applies_user_policy_visibility_toggles"
status: "draft"
---

## Related Files

- `app/javascript/packs/applyApplicationPolicyToggles.js`

## Functional Overview

On page load, the system fetches the current user's data and iterates over each policy object attached to that user. For each policy, it queries the DOM for all elements bearing the policy's associated CSS class name and either removes or adds the `hidden` class on each element according to whether the policy marks the feature as visible. This mechanism synchronises rendered HTML affordances — such as links and buttons for privileged features — with the server-side policy state for the authenticated user without re-rendering the page. Critically, the system does not rely on this client-side toggle for security enforcement; the server independently enforces the same policies on every request.

## Design Intent

The approach separates policy evaluation from rendering: the server emits policy metadata alongside user data, and the client mechanically applies CSS visibility changes based on that metadata. This keeps the toggle logic generic and "oblivious" to the specific features being toggled. Because security is enforced server-side, accidentally exposing a hidden element has no security consequence — it is purely a UX concern.

## Scenarios

### Policies present — visible feature

1. The page loads and the system requests the current user's data along with the CSRF token.
2. The user data includes a policies list; one policy has `visible: true` and a `dom_class` value that matches one or more elements in the page.
3. The system finds all DOM elements whose class list includes that `dom_class` value.
4. For each matching element, the system removes the `hidden` CSS class, making the element visible to the user.

### Policies present — hidden feature

1. The page loads and the system requests the current user's data along with the CSRF token.
2. A policy in the user's policy list has `visible: false` and a `dom_class` that matches one or more page elements.
3. The system finds all DOM elements carrying that `dom_class`.
4. For each matching element, the system adds the `hidden` CSS class, concealing the element from the user.

### No policies on the current user

1. The page loads and the system requests the current user's data.
2. The current user object carries no `policies` property or the property is falsy.
3. The system skips all DOM manipulation; no element visibility is altered.

### Policy dom_class matches no elements

1. A policy exists on the user with a `dom_class` that does not correspond to any element currently rendered in the page.
2. The system queries the DOM and receives an empty collection.
3. The loop body executes zero times; no error is raised and no visible change occurs.
