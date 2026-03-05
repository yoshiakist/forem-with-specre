---
id: "01KJXZPBZVARXP23QFJC190VM9"
name: "user_sees_loading_spinner"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/javascript/crayons/Spinner/Spinner.jsx`
- `app/javascript/crayons/Spinner/index.js`
- `app/javascript/crayons/Spinner/__tests__/Spinner.test.jsx` (Test)

## Functional Overview

The `Spinner` component renders an animated SVG loading indicator that communicates to the user that an asynchronous operation is in progress. It outputs a circular arc icon using the `crayons-icon` and `crayons-spinner` CSS classes, which drive the rotation animation via CSS. The SVG is marked `aria-hidden="true"` so screen readers ignore the decorative graphic, preserving accessibility for assistive technology users.

## Design Intent

The spinner is intentionally stateless and parameterless — it has no props — so it can be dropped into any loading context without configuration. By delegating visual sizing and animation entirely to CSS classes (`crayons-icon`, `crayons-spinner`), the component remains a pure presentational primitive and avoids encoding layout concerns in JavaScript.

## Key Members

- `crayons-icon` — CSS class that controls the base icon dimensions (24×24px viewBox)
- `crayons-spinner` — CSS class that applies the rotation keyframe animation
- `aria-hidden="true"` — prevents the decorative SVG from being announced by screen readers

## Scenarios

### User triggers a loading state

1. The application begins an asynchronous operation (e.g., a form submission or data fetch).
2. A parent component renders the `Spinner` component in place of or alongside the content area.
3. The user sees a rotating circular arc icon indicating activity is in progress.
4. When the operation completes, the parent component removes the `Spinner` from the DOM.

### Spinner is invisible to assistive technology

1. A screen reader user navigates to a page or component that is loading.
2. The `Spinner` SVG is rendered with `aria-hidden="true"`.
3. The screen reader ignores the spinner graphic entirely and does not announce it.
4. The user is not interrupted by meaningless decorative content.

### Spinner renders without accessibility violations

1. The `Spinner` component is rendered into the document.
2. An automated accessibility audit (axe) is run against the rendered output.
3. No accessibility violations are reported, confirming that the presentational SVG does not introduce ARIA or contrast issues.
