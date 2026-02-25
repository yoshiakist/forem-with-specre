---
id: "01KJBGTWBQSX8GE7QJS20WH3G6"
name: "system_applies_user_theme_on_page_load"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/decorators/user_decorator.rb`
- `app/views/layouts/_user_config.html.erb` (Template)
- `spec/decorators/user_decorator_spec.rb` (Test)

## Functional Overview

When a page is loaded, the system applies the user's previously saved theme and display preferences before the first paint, preventing a flash of unstyled or incorrectly themed content. The server-side `UserDecorator#config_body_class` method computes a space-separated string of CSS class tokens from the user's settings (theme, font, navbar style, moderation status, roles), and this string is persisted in `localStorage` by the client. On subsequent page loads, an inline script in `_user_config.html.erb` reads `config_body_class` from `localStorage` and immediately sets it as the document body's class, so the correct theme is active from the moment the DOM is ready. For dark theme users, the script also injects the full dark CSS inline and notifies any hosting native shell (React Native WebView) of the color mode. If the user has chosen the OpenDyslexic font, the script preloads that font file as an early resource hint.

## Design Intent

The inline script approach is intentional to eliminate theme flash: by acting before any CSS files are fetched and before React hydrates, the body class is set synchronously so the browser paints the first frame with the correct theme. Storing the class string in `localStorage` rather than a cookie avoids an extra round-trip to the server for every page, while the server-side decorator still acts as the single source of truth for what the class string should be after each login or settings change. The `ten-x-hacker-theme` alias is backfilled onto `dark_theme` to preserve compatibility with an older iOS native shell that keys off that legacy class name.

## Key Members

- `config_body_class` — the space-separated string of CSS class tokens written to `localStorage` and restored on load; built from the user's `config_theme`, resolved font name, navbar style, moderator status, trusted status, and assigned role names
- `config_body_class` in `localStorage` — client-side key read by the inline script on every page load
- `dark-mode-style` / `light-mode-style` — hidden `<div>` elements that hold the pre-rendered CSS text for each mode, injected into `body-styles` when the dark class is detected

## Scenarios

### Theme class applied before first paint

1. A returning user loads any page; the browser begins parsing the HTML.
2. The inline script runs synchronously and reads `config_body_class` from `localStorage`.
3. The script sets the value as `document.body.className` before any rendering occurs, ensuring the correct theme classes are active from the first paint.

### Dark theme CSS injected inline

1. The stored `config_body_class` contains `dark-theme`.
2. The inline script copies the pre-rendered dark CSS from the hidden `dark-mode-style` element into the `body-styles` element as a `<style>` tag.
3. If the page is running inside a React Native WebView, the script sends an `update_color_mode: dark` message to the native shell.

### Light theme notifies native shell

1. The stored `config_body_class` does not contain `dark-theme`.
2. If running inside a React Native WebView, the script sends an `update_color_mode: light` message to the native shell.

### OpenDyslexic font preloaded early

1. The stored `config_body_class` includes `open-dyslexic-article-body`.
2. The inline script creates a `<link rel="preload" as="font">` element pointing at the OpenDyslexic font file and appends it to `<head>`, ensuring the font download starts as early as possible.

### config_body_class built from user settings on server

1. The system decorates a user and calls `config_body_class`.
2. The method assembles tokens for the resolved theme (e.g., `light-theme`, `dark-theme`), the resolved font name (e.g., `sans-serif-article-body`), moderator status, trusted status, and navbar style.
3. For dark theme, the alias `ten-x-hacker-theme` is also appended for iOS native shell compatibility.
4. Each assigned role name is appended as a `user-role--<name>` token.
5. All tokens are joined with spaces and returned as the class string.

## Failures / Exceptions

- If `localStorage` is unavailable or throws (e.g., private browsing mode, storage quota), the entire inline script is wrapped in a `try/catch`; the error is reported to Honeybadger asynchronously after a 1-second delay, and the page renders with no body class pre-applied (the server-rendered defaults take over).
