---
id: "01KJXXSWNJZA876N5WNVPQRNS8"
name: "system_initializes_mobile_drawer_sidebar_navigation"
status: "draft"
---

## Related Files

- `app/javascript/packs/drawerSliders.js`

## Functional Overview

When the page contains on-page navigation controls, the system wires up click handlers for the mobile drawer sidebar overlay backgrounds and navigation buttons. Clicking an overlay background slides the corresponding sidebar out of view, while clicking a navigation button slides the corresponding sidebar into view. On each InstantClick page change, any open sidebars are dismissed and the `modal-open` CSS class is removed from the document body, ensuring a clean navigation state.

## Design Intent

Mobile drawer sidebars require explicit initialization at page load because the elements are rendered server-side and have no framework lifecycle hooks. Using `InstantClick.on('change', ...)` ensures sidebars are always reset on soft navigation, preventing stale open-drawer states from persisting across pages in the single-page-app style navigation pattern.

## Key Members

- `initializeDrawerSliders` — main setup function; checks for the `on-page-nav-controls` element before attaching any handlers, acting as a guard against running on pages without the drawer UI
- `slideSidebar(side, direction)` — global function (declared elsewhere) that performs the actual CSS transition for the given `side` (`'left'` or `'right'`) and `direction` (`'intoView'` or `'outOfView'`)
- `on-page-nav-controls` — sentinel element; its presence indicates the current page includes the drawer navigation UI
- `sidebar-bg-left` / `sidebar-bg-right` — overlay background elements; clicking either dismisses the respective sidebar
- `on-page-nav-butt-left` / `on-page-nav-butt-right` — button elements that open the left or right sidebar respectively
- `InstantClick` — soft-navigation library; the `change` event fires before a new page is rendered

## Scenarios

### Page includes drawer navigation controls

1. Page load completes and `initializeDrawerSliders` is called.
2. The system detects the `on-page-nav-controls` element on the page.
3. The system attaches an `onclick` handler to `sidebar-bg-left` that calls `slideSidebar('left', 'outOfView')`.
4. The system attaches an `onclick` handler to `sidebar-bg-right` that calls `slideSidebar('right', 'outOfView')`.
5. The system attaches an `onclick` handler to `on-page-nav-butt-left` that calls `slideSidebar('left', 'intoView')`.
6. The system attaches an `onclick` handler to `on-page-nav-butt-right` that calls `slideSidebar('right', 'intoView')`.
7. The system registers an `InstantClick` `change` listener that resets drawer state on soft navigation.

### User opens the left sidebar

1. User taps the left navigation button (`on-page-nav-butt-left`).
2. The click handler fires and calls `slideSidebar('left', 'intoView')`.
3. The left sidebar slides into view.

### User dismisses the left sidebar via overlay

1. User taps the left overlay background (`sidebar-bg-left`).
2. The click handler fires and calls `slideSidebar('left', 'outOfView')`.
3. The left sidebar slides out of view.

### User opens the right sidebar

1. User taps the right navigation button (`on-page-nav-butt-right`).
2. The click handler fires and calls `slideSidebar('right', 'intoView')`.
3. The right sidebar slides into view.

### User dismisses the right sidebar via overlay

1. User taps the right overlay background (`sidebar-bg-right`).
2. The click handler fires and calls `slideSidebar('right', 'outOfView')`.
3. The right sidebar slides out of view.

### InstantClick navigates to a new page

1. InstantClick fires its `change` event before rendering the new page.
2. The system removes `modal-open` from `document.body`'s class list.
3. The system calls `slideSidebar('right', 'outOfView')` to close the right sidebar.
4. The system calls `slideSidebar('left', 'outOfView')` to close the left sidebar.
5. The new page renders with all sidebars dismissed.

## Failures / Exceptions

- If `on-page-nav-controls` is absent from the page, `initializeDrawerSliders` exits immediately and no handlers are attached.
- Individual overlay or button elements are checked for existence before binding handlers; if any element is absent, the remaining elements are still wired up normally.
