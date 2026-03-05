---
id: "01KJXTKB2CSQZ15XV5RZ3S3YXC"
name: "system_provides_base_record_utilities_for_all_models"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/models/application_record.rb`
- `spec/models/application_record_spec.rb` (Test)

## Functional Overview

`ApplicationRecord` is the abstract base class for every Active Record model in the application. In addition to the decorator and purgeable concerns covered by separate cards, it supplies five cross-cutting utilities available to all subclasses: `estimated_count` reads PostgreSQL's planner statistics to return an approximate row count without a full sequential scan; `with_statement_timeout` temporarily overrides the database statement timeout for a block and unconditionally restores it on exit; `with_synchronous_commit_off` wraps a block in a transaction with `synchronous_commit = OFF` to improve throughput for high-volume inserts; `find_each_respecting_scope` and `in_batches_respecting_scope` are scope-aware batch iterators that honour arbitrary `WHERE`, `ORDER`, `LIMIT`, and `OFFSET` clauses — unlike Rails' built-in `find_each`, which ignores custom ordering; and `errors_as_sentence` (exposed as `errors_as_sentence` on instances) formats Active Model validation errors as a single human-readable sentence.

## Design Intent

Placing these utilities directly on `ApplicationRecord` rather than in stand-alone service objects or concern modules makes them available uniformly to every model without any per-class include. `estimated_count` trades exact accuracy for speed on very large tables where a `COUNT(*)` would be prohibitively slow. `with_statement_timeout` provides a safe, restoring wrapper so callers never accidentally leave a tighter-than-intended timeout in place. The scope-respecting batch methods were introduced because Rails' `find_each` silently ignores custom ordering, which caused correctness problems for ordered exports and background jobs; the implementation snapshots IDs up-front so the ordering stays stable across pages even if rows are inserted concurrently. `with_synchronous_commit_off` acknowledges that durability guarantees can be relaxed for certain bulk operations to avoid write-amplification and WAL pressure.

## Key Members

- `QUERY_ESTIMATED_COUNT` — frozen SQL string that queries `pg_class` statistics to compute the estimated row count for a named table.
- `estimated_count` (class method) — executes `QUERY_ESTIMATED_COUNT` for the model's own table and returns an integer estimate.
- `with_statement_timeout(duration, connection:)` (class method) — sets the per-session `statement_timeout` to `duration` (in seconds), yields, and restores the original value in an `ensure` block.
- `with_synchronous_commit_off` (class method) — opens a transaction, sets `LOCAL synchronous_commit TO OFF`, and yields.
- `in_batches_respecting_scope(batch_size: 1000)` (class method) — collects all matching IDs in order, then yields successive arrays of records in groups of `batch_size`.
- `find_each_respecting_scope(batch_size: 1000)` (class method) — wraps `in_batches_respecting_scope` to yield individual records; returns an `Enumerator` when called without a block.
- `errors_as_sentence` (instance method) — returns `errors.full_messages` joined as a natural-language sentence.

## Scenarios

### Retrieving an estimated row count

1. A caller invokes `SomeModel.estimated_count`.
2. The system queries PostgreSQL's `pg_class` catalogue using pre-computed planner statistics (tuples-per-page × number-of-pages).
3. The method returns an integer approximation of the row count and releases the `PG::Result` immediately to free memory.
4. If the table has no pages yet, the denominator is clamped to 1 so no division-by-zero occurs.

### Setting a temporary statement timeout

1. A caller invokes `SomeModel.with_statement_timeout(5.seconds) { ... }`.
2. The system reads the current `statement_timeout` setting from PostgreSQL before making any change.
3. The system sets `statement_timeout` to 5000 ms for the current connection.
4. The block executes; any statement that runs longer than 5 seconds raises a `StatementTimeout` error.
5. In the `ensure` clause the system unconditionally restores the original timeout, even if the block raised an error.
6. Nesting `with_statement_timeout` calls is supported: each level saves and restores its own previous value.

### Disabling synchronous commit for high-volume inserts

1. A caller invokes `SomeModel.with_synchronous_commit_off { ... }`.
2. The system opens a database transaction and sets `synchronous_commit = OFF` for the duration of that transaction.
3. The block performs its inserts; PostgreSQL does not wait for WAL records to be flushed to disk before acknowledging each write.
4. The transaction commits (or rolls back on error), and the session reverts to its default synchronous-commit setting automatically because `LOCAL` was used.

### Batch-processing records while respecting an arbitrary scope

1. A caller applies a scope with a custom `ORDER`, `WHERE`, or `LIMIT`/`OFFSET` clause and calls `in_batches_respecting_scope(batch_size: N)`.
2. The system executes a single query to collect all matching IDs in the correct order, then discards the `WHERE`, `ORDER`, `LIMIT`, and `OFFSET` clauses from the batch relation to avoid conflicts.
3. The system groups the IDs into slices of at most `N` and, for each slice, fetches the corresponding records by primary key in a cache-bypassing query.
4. The system yields each batch as an array, preserving the original ordering and skipping any IDs that no longer exist.
5. `find_each_respecting_scope` delegates to `in_batches_respecting_scope` and yields individual records rather than arrays. When called without a block it returns a lazy `Enumerator` and defers all database queries until iteration begins.

### Formatting validation error messages

1. A caller invokes `record.errors_as_sentence` after a failed validation.
2. The system collects all full validation error messages from the model's `errors` object and joins them into a single English sentence using Active Support's `to_sentence`.
3. The resulting string is returned to the caller for display or logging.

## Failures / Exceptions

- If `estimated_count` is called on a model whose table does not yet exist in `pg_class`, the query returns zero rows and `result.first` would be `nil`, potentially raising a `NoMethodError`. Callers should guard against this when the table may not exist (e.g., in migrations).
- If the block passed to `with_statement_timeout` raises an error, the `ensure` block still restores the original timeout, so the connection is left in a consistent state.
- `in_batches_respecting_scope` loads all matching IDs into memory up-front; for extremely large result sets this may consume significant memory. Callers should apply appropriate `WHERE` scopes to limit the working set.
- If a record is deleted between the initial ID snapshot and the batch fetch, it is silently omitted from the yielded array rather than raising an error.
