---
id: "01KJXWGP0V021QH50BJW9Q1KKD"
name: "user_can_create_listing"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/models/listing.rb`
- `app/controllers/concerns/api/listings_controller.rb`
- `app/controllers/api/v0/listings_controller.rb`
- `app/controllers/api/v1/listings_controller.rb`
- `app/javascript/listings/listingForm.jsx`
- `app/javascript/listings/components/Title.jsx`
- `app/javascript/listings/components/BodyMarkdown.jsx`
- `app/javascript/listings/components/Categories.jsx`
- `app/javascript/listings/components/ListingTagsField.jsx`
- `app/javascript/listings/components/ExpireDate.jsx`
- `app/javascript/packs/listingForm.jsx`
- `app/javascript/listings/__tests__/BodyMarkdown.test.jsx` (Test)
- `app/javascript/listings/__tests__/ListingTagsField.test.jsx` (Test)

## Functional Overview

A logged-in user can create a new classified listing by filling in a form that collects a title (up to 128 characters), a markdown body (up to 400 characters), a category, up to 8 tags, and an optional expiry date. The frontend `ListingForm` component detects whether the listing is new (no `id`) and renders the full creation form with all fields. Category-specific tag suggestions are surfaced in the tags autocomplete field. The form may optionally be submitted on behalf of an organization if the user belongs to one. Both the v0 and v1 API controllers require authentication via API key or current session before accepting a create request.

## Design Intent

The form distinguishes between create and edit modes based on the presence of an `id` in the listing prop, rendering a richer set of fields (category picker, expiry date) only during creation. Category-aware tag suggestions are derived client-side from a predefined map keyed by `categorySlug`, avoiding a server round-trip for common tag recommendations while still supporting full Algolia-backed search for arbitrary tags.

## Key Members

- `title` — plain text, 128 characters max
- `bodyMarkdown` — markdown content, 400 characters max, no images
- `categoryId` / `categorySlug` — selected listing category identifier and slug
- `tagList` — comma-separated tag string, up to 8 tags
- `expireDate` — optional ISO date between tomorrow and 30 days from today
- `organizationId` — optional; when set, the listing is posted under the organization

## Scenarios

### User creates a new listing

1. The user navigates to the new listing page; the frontend detects no existing `id` and renders the full creation form.
2. The user enters a title (up to 128 characters) and a markdown body (up to 400 characters).
3. The user selects a category from the dropdown; the tags field immediately updates its category-specific top-tag suggestions.
4. The user optionally adds up to 8 tags using the autocomplete field, which blends category-specific suggestions with Algolia search results.
5. The user optionally sets a custom expiry date between tomorrow and 30 days ahead.
6. If the user belongs to one or more organizations, they can choose to post under an organization; doing so spends the organization's credits.
7. The user submits the form; the controller (v0 or v1) authenticates via API key or current session and creates the listing.

### Category-specific tag suggestions are shown

1. The user focuses the tags input field.
2. The component looks up the current `categorySlug` in the predefined `additionalTags` map (covering categories such as `jobs`, `forhire`, `forsale`, `events`, `collabs`).
3. Matching category tags are displayed under a "Top tags" heading alongside any Algolia search results.
4. Selecting a suggested tag adds it to the tag list; the hidden input reflects the updated comma-separated value for form submission.

### API create endpoint requires authentication

1. A request reaches `POST /api/v0/listings` or `POST /api/v1/listings`.
2. The `authenticate_with_api_key_or_current_user!` before-action runs and verifies the requester's identity.
3. If authentication succeeds, the create action proceeds and returns HTTP 200.

## Failures / Exceptions

- Unauthenticated requests to the create endpoint are rejected by `authenticate_with_api_key_or_current_user!` before the action body is reached.
- The body markdown field enforces a 400-character limit and does not allow images (enforced client-side via field description and `maxLength` attribute).
- The expiry date input constrains selection to the range from tomorrow through 30 days hence (enforced via `min`/`max` attributes).
