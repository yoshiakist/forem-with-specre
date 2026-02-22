---
id: "01KJ1C2A7B86GEDA127PKWJ999"
name: "system_detects_viewport_breakpoints"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/javascript/shared/components/useMediaQuery.js`
- `app/javascript/shared/components/MediaQuery.jsx`
- `app/javascript/shared/components/__tests__/useMediaQuery.test.js` (Test)
- `app/javascript/shared/components/__tests__/MediaQuery.test.jsx` (Test)

## Functional Overview

The system provides two complementary primitives for reactive viewport detection. A `BREAKPOINTS` constant maps named size tiers (`Small`, `Medium`, `Large`, `ExtraLarge`) to pixel widths copied from the project's SCSS variables. The `useMediaQuery` hook wraps the browser's `window.matchMedia` API to evaluate an arbitrary CSS media query string, initialises state from the current match result, and keeps state in sync by registering a listener that updates whenever the viewport changes; the listener is removed on cleanup to prevent memory leaks. The `MediaQuery` component provides a declarative render-prop interface over the same hook, accepting a `query` string and a `render` function and delegating the match boolean to that function so callers can conditionally render UI without managing the hook directly.

## Design Intent

The hook and component are intentionally separate so that consumers can use the raw boolean from `useMediaQuery` in any imperative logic (class guards, conditional returns) while `MediaQuery` satisfies the common render-prop pattern with minimal boilerplate. `BREAKPOINTS` mirrors the SCSS variables to keep JS and CSS breakpoint definitions in sync from a single source of truth.

## Key Members

- `BREAKPOINTS` — frozen object with pixel-width values for `Small` (640), `Medium` (768), `Large` (1024), and `ExtraLarge` (1280)
- `query: string` — a CSS media query string passed to `window.matchMedia` (e.g. `(width >= 768px)`)
- `render: func` — a render-prop function that receives the current match boolean and returns JSX

## Scenarios

### Hook reflects a non-matching query

1. A component calls `useMediaQuery` with a CSS media query string.
2. The browser reports that the current viewport does not match the query.
3. The hook returns `false`.
4. A change listener is registered on the `matchMedia` object.
5. When the component unmounts, the listener is removed.

### Hook reflects a matching query

1. A component calls `useMediaQuery` with a CSS media query string.
2. The browser reports that the current viewport matches the query.
3. The hook returns `true`.
4. A change listener is registered on the `matchMedia` object.
5. When the component unmounts, the listener is removed.

### Component delegates match result to render prop

1. A parent renders `<MediaQuery>` with a `query` string and a `render` function.
2. `MediaQuery` evaluates the query via `useMediaQuery`.
3. The `render` function is called with the current match boolean as its argument.
4. The return value of `render` is used as the rendered output.
