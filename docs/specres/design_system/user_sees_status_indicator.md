---
id: "01KJXZKS5PJJSC8V8DZAGDWVFV"
name: "user_sees_status_indicator"
status: "draft"
---

## Related Files

- `app/javascript/crayons/Indicators/Indicator.jsx`
- `app/javascript/crayons/Indicators/index.js`

## Functional Overview

The `Indicator` component renders a styled inline `<span>` badge that communicates a status or category to the user. It accepts a `variant` prop that maps to one of five semantic values — `default`, `info`, `success`, `warning`, or `danger` — and applies the corresponding CSS modifier class (e.g., `c-indicator--warning`). When no variant is supplied, only the base `c-indicator` class is applied. An optional `extraPadding` boolean adds a `p-2` utility class for contexts that require more visual breathing room. Any `children` passed to the component are rendered as the badge label.

## Design Intent

The component is intentionally minimal and presentation-only: it holds no state and delegates all visual differentiation to CSS class names following BEM conventions. This keeps the component decoupled from application logic and lets the design system control appearance through a single stylesheet, making it easy to theme or reskin without touching component code.

## Key Members

- `variant: 'default' | 'info' | 'success' | 'warning' | 'danger'` — selects the semantic color scheme; defaults to `'default'`, which applies no modifier class
- `extraPadding: boolean` — when `true`, adds `p-2` utility class for increased horizontal/vertical padding
- `className: string` — allows callers to append additional CSS classes for one-off overrides
- `children` — the text or node rendered inside the badge span

## Scenarios

### User views a badge with no variant specified

1. A page renders `<Indicator>` without a `variant` prop.
2. The component applies only the base `c-indicator` class to the `<span>`.
3. The badge is displayed using the default styling with no semantic color modification.

### User views a badge with a semantic variant

1. A page renders `<Indicator variant="warning">Needs review</Indicator>`.
2. The component applies both `c-indicator` and `c-indicator--warning` classes.
3. The badge appears with the warning color scheme, visually signaling caution to the user.

### User views a badge with extra padding enabled

1. A component renders `<Indicator variant="success" extraPadding>Published</Indicator>`.
2. The component applies `c-indicator`, `c-indicator--success`, and `p-2` classes.
3. The badge is displayed with the success style and increased padding, giving it more visual weight in its context.

### User views a badge with a custom class

1. A caller renders `<Indicator variant="info" className="mt-2">Beta</Indicator>`.
2. The component applies `c-indicator`, `c-indicator--info`, and `mt-2` classes.
3. The badge appears with the info style and the caller-supplied margin, fitting naturally into its surrounding layout.
