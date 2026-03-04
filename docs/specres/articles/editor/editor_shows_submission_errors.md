---
id: "01KJV0FG4SVVE94D8VGYYQE8YY"
name: "editor_shows_submission_errors"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/javascript/article-form/components/ErrorList.jsx`
- `app/javascript/article-form/articleForm.jsx`
- `app/javascript/article-form/actions.js`
- `app/javascript/article-form/components/__tests__/Form.test.jsx` (Test)

## Functional Overview

When `submitArticle` receives an error response (HTTP 422 or 429), it calls the `onError` callback with the parsed error object. `ArticleForm`'s error handler sets `errors` in state and scrolls the form to the top. `Form` renders `<ErrorList errors={errors} />` whenever `errors` is non-null. `ErrorList` iterates `Object.keys(errors)` and renders each entry as a list item; entries whose key is `"base"` display the message alone, while others display `"<key>: <message>"`.

## Design Intent

Errors are surfaced immediately at the top of the form so authors can see all problems at once before re-editing. The `base` key convention matches Rails' `errors.add(:base, ...)` pattern, letting the backend communicate non-field-specific messages (e.g., rate-limit text) without special-casing in the frontend.

## Key Members

- `ErrorList({ errors })` — pure component; renders a danger notice with a `<ul>` of error messages
- `ArticleForm` error handler — sets `{ submitting: false, errors }` and scrolls to top
- `submitArticle` — calls `onError(errors)` on a non-2xx response

## Scenarios

### Submission fails with validation errors (HTTP 422)

1. Author submits an article with invalid fields (e.g., blank `body_markdown`).
2. Server returns HTTP 422 with `{ errors: { body_markdown: "can't be blank" } }`.
3. `submitArticle` calls `onError({ body_markdown: "can't be blank" })`.
4. `ArticleForm` sets `errors` in state; the form scrolls to the top.
5. `ErrorList` renders: `body_markdown: can't be blank`.

### Submission blocked by rate limit (HTTP 429)

1. Author submits but exceeds the rate limit.
2. Server returns HTTP 429 with a `{ error: "..." }` body and a `Retry-After` header.
3. `ArticleForm` renders `ErrorList` with the rate-limit message.

## Failures / Exceptions

- If the server returns an unexpected non-JSON body, `submitArticle` surfaces a generic error message to avoid a silent failure.
