---
id: "01KJXXQCH4J8E98SGR04CZ6DK3"
name: "system_hides_blocked_and_low_quality_content"
status: "draft"
---

## Related Files

- `app/javascript/packs/contentDisplayPolicy.js`
- `app/javascript/contentDisplayPolicy/hideBlockedContent.js`
- `app/javascript/contentDisplayPolicy/initHiddenComments.js`

## Functional Overview

On every page load and on each InstantClick navigation event, the system enforces two content visibility rules. First, it scans the DOM for articles and comments authored by users the current viewer has blocked, then hides those articles entirely or replaces comment bodies with a "[blocked content]" placeholder. Second, it wires up hide/unhide controls for low-quality comments: a moderator-facing hide button opens a confirmation modal (with an optional "hide children" checkbox) that submits a PATCH request to hide the comment, and a corresponding unhide link submits a PATCH request to reveal it again; after either action succeeds the page reloads to reflect the updated state.

## Design Intent

Separating content suppression into two focused modules (`hideBlockedContent` and `initHiddenComments`) keeps blocked-user logic independent from moderation workflows. Running both functions at initial page load and on every InstantClick `change` event ensures that client-side navigation (which replaces DOM content without a full page reload) also applies the same visibility rules.

## Scenarios

### Blocked user's article is hidden on page load

1. The current user has one or more blocked user IDs in their `userData` global.
2. The page contains one or more `<article data-content-user-id="...">` elements whose `data-content-user-id` matches a blocked ID and whose class includes `crayons-story`.
3. The system sets `display: none` on each matching article so it is not visible to the viewer.

### Blocked user's comment body is replaced on page load

1. The current user has one or more blocked user IDs in their `userData` global.
2. The page contains a comment node (`single-comment-node`) whose `data-content-user-id` matches a blocked ID.
3. The system replaces the `.inner-comment` element's HTML with a dimmed, non-selectable "[blocked content]" placeholder instead of hiding the entire node.

### Moderator hides a low-quality comment via modal

1. The rendered page includes one or more elements with class `hide-comment` that carry `data-comment-id` and `data-comment-url` attributes.
2. The viewer clicks a hide button; the system prevents the default action and opens a `Forem.showModal` confirmation dialog titled "Confirm hiding the comment".
3. The modal form action is set to `/comments/:id/hide`, a report-abuse link and a permalink are populated with the comment's URL.
4. The viewer optionally checks "hide children" and submits the form.
5. The system sends `PATCH /comments/:id/hide` (appending `?hide_children=1` when checked) with the CSRF token.
6. If the server responds with `hidden: "true"`, the page reloads.

### Moderator unhides a previously hidden comment

1. The rendered page includes one or more elements with class `unhide-comment` that carry a `data-comment-id` attribute.
2. The viewer clicks an unhide link; the system prevents the default action and sends `PATCH /comments/:id/unhide` with the CSRF token.
3. If the server responds with `hidden: "false"`, the page reloads.

### Rules are re-applied after InstantClick navigation

1. InstantClick replaces the page DOM on a `change` event (client-side navigation).
2. The system calls `hideBlockedContent()` and `initHiddenComments()` again so that blocked content is hidden and comment controls are re-wired for the newly loaded content.
