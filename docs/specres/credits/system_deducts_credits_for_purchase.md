---
id: "01KJ2SJMM4QCT6P9M0K1K4HTAT"
name: "system_deducts_credits_for_purchase"
status: "draft"
---

## Related Files

- `app/services/credits/buy.rb`
- `app/models/credit.rb`

## Functional Overview

When a purchaser initiates a credit-based transaction, `Credits::Buy` verifies that the purchaser holds enough unspent credits to cover the cost. If sufficient credits are available, it atomically marks exactly that many unspent credits as spent, stamping each with the current time and the identity of the purchase target (polymorphic association). The purchaser's cached aggregate columns are then updated via a `save` call. If the purchaser lacks sufficient credits, the operation is aborted immediately and returns `false` without modifying any records.

## Design Intent

Deducting credits by updating existing `Credit` records (rather than deleting them and inserting negative entries) preserves a full audit trail of every credit's lifecycle — when it was created, when it was spent, and what it was spent on. The polymorphic `purchase_type` / `purchase_id` columns allow a single credits ledger to reference any purchasable entity without schema changes. Returning a plain boolean from `Credits::Buy.call` keeps call-sites simple and avoids exception-based control flow for an expected "not enough credits" condition.

## Key Members

- `purchaser` — A `User` or `Organization` that owns the credits; must respond to `enough_credits?(cost)` and have a `credits` association.
- `purchase` — Any ActiveRecord object representing the thing being purchased; its class name and id are stored on each deducted credit.
- `cost` — Integer number of credits required for the purchase.
- `Credit#spent` — Boolean flag on each credit record indicating whether it has been consumed.
- `Credit.spent` / `Credit.unspent` — Named scopes used to filter credit records by their consumption state.

## Scenarios

### Successful credit deduction

1. A purchaser with enough unspent credits calls `Credits::Buy.call` with the target purchase and the required cost.
2. The system verifies the purchaser has at least `cost` unspent credits.
3. The system selects exactly `cost` unspent credit records and updates them in a single bulk operation, marking each as spent and recording the current timestamp and the purchase's type and id.
4. The purchaser record is saved to synchronize any counter-cache columns maintained by the model.
5. The operation returns `true` to the caller.

### Insufficient credits — purchase blocked

1. A purchaser whose unspent credit balance is less than `cost` calls `Credits::Buy.call`.
2. The system checks the balance and finds it insufficient.
3. No credit records are modified.
4. The operation returns `false` immediately.

### Credits marked with purchase identity

1. After a successful deduction, each of the consumed `Credit` records carries the `purchase_type` (the class name of the purchased object) and `purchase_id` (its id).
2. This allows any part of the system to trace which purchase consumed a given credit.

## Failures / Exceptions

- If `purchaser.enough_credits?(cost)` returns falsy, `Credits::Buy.call` returns `false` and halts without touching the database — the caller is responsible for handling this case.
- No negative credit balance is created; credits can only be deducted down to zero.
