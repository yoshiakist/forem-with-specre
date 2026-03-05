---
id: "01KJ2SFDGGZ68ZN4F9V15YW4KV"
name: "user_can_view_credit_ledger"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/credits_controller.rb`
- `app/services/credits/ledger.rb`
- `spec/requests/credits_spec.rb` (Test)
- `app/views/credits/index.html.erb` (Template)
- `app/views/credits/_ledger.html.erb` (Template)
- `app/views/credits/_ledger_listing.html.erb` (Template)
- `app/views/credits/_ledger_sponsorship.html.erb` (Template)

## Functional Overview

When an authenticated user visits the credits index page, the system counts their unspent credits and assembles a purchase history ledger using `Credits::Ledger`. The ledger is built for the user and for every organization the user administers. Each ledger entry groups spent credits by the associated purchase (e.g., a `Listing`), capturing the item, credit cost, and date. Spent credits with no associated purchase are lumped together as a single miscellaneous entry. The view renders each entity's unspent count, a link to purchase more credits, and a "Purchase history" table showing individual and unattributed spend.

## Design Intent

The ledger avoids N+1 queries by grouping spent credits by `purchase_type` and loading each purchase model in one batch per type. Credits without a `purchase_type` are aggregated into a single entry rather than shown individually, keeping the ledger concise for situations like promotional credit grants.

## Key Members

- `Credits::Ledger::Item` — value struct holding `purchase` (the associated model or nil), `cost` (integer), and `purchased_at` (timestamp). Used to populate ledger table rows.
- `@user_unspent_credits_count` — integer count of the current user's unspent credits, shown in the page header.
- `@ledger` — a hash keyed by `[entity_class_name, entity_id]` arrays (e.g., `["User", 42]` or `["Organization", 7]`), with each value being an ordered array of `Item` structs for that entity.
- `@organizations` — the list of organizations for which the current user is an admin; controls whether org ledger sections appear.

## Scenarios

### Authenticated user views their credit balance and purchase history

1. An authenticated user navigates to `GET /credits`.
2. The system counts the user's unspent credits and builds a ledger of their spent credits grouped by purchase.
3. The page displays the user's unspent credit count and a link to purchase more credits.
4. If the user has spent credits, a "Purchase history" table is rendered showing each purchase's category, item link, credit cost, and date.

### Org admin also sees organization credit sections

1. An authenticated user who is an admin of one or more organizations visits `GET /credits`.
2. The system builds ledger entries for each administered organization in addition to the user's own ledger.
3. The page displays a separate credit section for each organization, showing the org's unspent credit count and its own "Purchase history" table.

### Org member (non-admin) does not see org credit section

1. An authenticated user who is a member but not an admin of an organization visits `GET /credits`.
2. Because the user holds no admin role in any organization, `@organizations` is empty.
3. The page shows only the user's personal credit balance and purchase history; no organization section is rendered.

### Spent credits with no associated purchase appear as miscellaneous

1. A user has spent credits that are not linked to any specific purchase record (e.g., promotional credits used without a purchaseable item).
2. The ledger aggregates these into a single row with the total cost and displays "Miscellaneous items" as the item label, with no category or date.

### Linked purchases render with type-specific partials

1. A user has spent credits on a `Listing` purchase.
2. The ledger groups those credits by purchase ID and loads the associated `Listing` records in one batch.
3. Each `Listing` item is displayed with the category label "Listing" and a truncated link to the listing's page rendered via the `_ledger_listing` partial.
