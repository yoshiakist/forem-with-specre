---
id: "01KJXZ9HXPZXY1JNTPC27CV31K"
name: "user_can_trigger_actions_via_button"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/Button/Button.jsx`
- `app/javascript/crayons/Button/index.js`
- `app/javascript/crayons/Buttons/Button.jsx`
- `app/javascript/crayons/Buttons/index.js`
- `app/javascript/crayons/Button/__tests__/Button.test.jsx` (Test)
- `app/javascript/crayons/Buttons/__tests__/Buttons.test.jsx` (Test)

## Functional Overview

The crayons design system provides two button component implementations — the legacy `Button` and the current `ButtonNew` — that render interactive button elements with configurable variants, sizes, icon positions, disabled/destructive states, and optional tooltip support. Both components apply CSS class names dynamically based on their props, forward interaction event handlers (click, focus, blur, keyboard), and suppress an attached tooltip when the user presses Escape. The legacy `Button` additionally supports rendering as an anchor tag (`<a>`) for link-style buttons, while `ButtonNew` uses the `classnames` library and the shared `Icon` component for a simpler, more focused API.

## Design Intent

Two parallel implementations exist because `ButtonNew` is a redesigned successor to the legacy `Button`. The legacy component remains in use to avoid breaking existing call sites; new surfaces are expected to adopt `ButtonNew`. Tooltip suppression on Escape follows keyboard accessibility best practices, allowing users to dismiss tooltips without navigating away from the button.

## Key Members

- `variant` — controls the visual style; legacy supports `primary`, `secondary`, `outlined`, `danger`, `ghost-*`; `ButtonNew` supports `default`, `primary`, `secondary`
- `contentType` (legacy only) — controls icon placement relative to label: `text`, `icon-left`, `icon-right`, `icon`, `icon-rounded`
- `icon` — a component or element type rendered as an inline icon
- `destructive` (`ButtonNew` only) — applies a destructive style modifier independent of variant
- `rounded` (`ButtonNew` only) — applies full-radius rounding
- `tagName` (legacy only) — renders the button as either a `<button>` or `<a>` element
- `tooltip` — node or string rendered as a floating tooltip inside the button; suppressed on Escape key
- `suppressTooltip` — internal state flag; set to `true` when Escape is pressed, hiding the tooltip span

## Scenarios

### Rendering with a visual variant

1. A consumer renders a button with a `variant` prop such as `secondary`, `danger`, or `primary`.
2. The component adds the corresponding CSS modifier class (e.g., `crayons-btn--secondary` or `c-btn--primary`) to the root element.
3. The button displays with the correct visual style for that variant.

### Rendering with an icon

1. A consumer passes an `icon` prop (and, for the legacy component, a `contentType` of `icon-left`, `icon-right`, or `icon`).
2. The component places the icon element before or after the label text according to the content type, or alone when no children are provided.
3. `ButtonNew` always renders the icon before the label and applies `c-btn--icon-left` when children are present, or `c-btn--icon-alone` when no label is given.

### Disabling the button

1. A consumer sets `disabled` to `true`.
2. The legacy `Button` adds `crayons-btn--disabled` to its class list and, when rendered as an anchor, omits the `href` attribute to prevent navigation.
3. The native `<button>` element receives the `disabled` attribute, making it non-interactive.

### Triggering an action on click or focus event

1. A consumer attaches an `onClick`, `onFocus`, `onBlur`, `onMouseOver`, or `onMouseOut` handler to the button.
2. When the user performs the corresponding interaction, the component fires the handler exactly once.
3. `ButtonNew` forwards all additional props (including event handlers) directly to the underlying `<button>` element via spread.

### Suppressing a tooltip on Escape

1. A consumer renders a button with a `tooltip` prop; the tooltip span is visible when the button has focus.
2. The user presses the Escape key while the button is focused.
3. The component sets its internal `suppressTooltip` state to `true`, adding `crayons-tooltip__suppressed` to the tooltip span and visually hiding it.
4. Any `onKeyUp` handler passed by the consumer is also called during this interaction.
