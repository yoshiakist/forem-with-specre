---
id: "01KJ246P62P50ED5YJNGJ50J3J"
name: "system_ranks_feed_articles_using_configurable_levers"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/models/articles/feeds/lever_catalog_builder.rb`
- `app/models/articles/feeds/order_by_lever.rb`
- `app/models/articles/feeds/relevancy_lever.rb`
- `app/models/articles/feeds/variant_assembler.rb`
- `app/services/articles/feeds/variant_query.rb`
- `spec/models/articles/feeds/lever_catalog_builder_spec.rb` (Test)
- `spec/models/articles/feeds/order_by_lever_spec.rb` (Test)
- `spec/models/articles/feeds/relevancy_lever_spec.rb` (Test)
- `spec/models/articles/feeds/variant_assembler_spec.rb` (Test)
- `spec/services/articles/feeds/variant_query_spec.rb` (Test)

## Functional Overview

The system ranks feed articles by computing a relevancy score for each article using a set of named, configurable levers. A `LeverCatalogBuilder` registers two types of levers at startup: `RelevancyLever` objects that contribute SQL SELECT fragments and scoring case-weights to the score, and `OrderByLever` objects that define how the final result set is sorted. A named feed variant (a JSON file under `config/feed-variants/`) declares which relevancy levers to activate, their scoring cases and fallback weights, and which order-by lever to apply. `VariantAssembler` reads the variant JSON, fetches and configures the declared levers from the catalog, and assembles a `VariantQuery::Config`. `VariantQuery` then uses that config to build a parameterized SQL sub-query that multiplies the active lever scores together into a single `relevancy_score`, filters articles by publication recency and score floor, and returns an `ActiveRecord::Relation` ordered by the chosen sort lever.

## Design Intent

Levers are registered once at boot and frozen immediately, making the catalog immutable after initialization. This prevents accidental runtime mutation and allows safe concurrent access. Variant configurations are loaded from JSON files rather than being hard-coded, so new scoring experiments can be deployed by adding a file without changing application code. The relevancy score is the product of all active lever scores rather than a sum, which means any lever returning a near-zero weight can suppress an article entirely. A stable randomizer seed (cached per user) provides variety without changing article order on every page refresh, with an escape hatch via a feature flag or explicit seed override.

## Key Members

- `RelevancyLever` — describes one scoring dimension: a SQL SELECT fragment, optional JOIN and GROUP BY fragments, whether a signed-in user is required, and the names of any query parameters the fragment needs.
- `RelevancyLever::Configured` — the result of calling `configure_with` on a lever; holds the resolved cases array, fallback numeric weight, and extracted query parameter values ready for injection into SQL.
- `OrderByLever` — holds a SQL ORDER fragment and exposes it as an Arel-safe SQL value via `to_sql`.
- `VariantQuery::Config` — a value object passed to `VariantQuery` containing the resolved lever list, order-by lever, maximum publication age, and whether the randomizer seed should be refreshed on each request.
- `VariantAssembler::DIRECTORY` — the Rails-root-relative path (`config/feed-variants`) where variant JSON files are stored.

## Scenarios

### Building the lever catalog at boot

1. The application initializes a `LeverCatalogBuilder` by passing a configuration block.
2. Inside the block, the builder registers each relevancy lever (key, label, SQL fragments, user-required flag) and each order-by lever (key, label, SQL ORDER fragment).
3. After the block executes, both lever registries are frozen, making the catalog read-only for the lifetime of the process.
4. Any attempt to register a lever with a key already present raises `LeverCatalogBuilder::DuplicateLeverError`.

### Assembling a variant configuration from a JSON file

1. A caller requests a variant by name (e.g., `"20230601-variant"`) via `VariantAssembler.call`.
2. The assembler looks up the variant in its in-memory cache; on a miss, it reads the corresponding JSON file from `config/feed-variants/`, caching the raw hash in Rails.cache keyed on the variant name and the current deploy commit ID.
3. For each lever entry declared in the JSON, the assembler fetches the matching `RelevancyLever` from the catalog by key and calls `configure_with`, passing the declared cases array, fallback weight, and any named query parameters.
4. The assembler constructs and returns a `VariantQuery::Config` containing the configured levers, the resolved `OrderByLever`, the maximum publication age in days, and the randomizer-reseed flag.
5. If the variant file does not exist, an `Errno::ENOENT` error is raised; if a declared lever key is absent from the catalog, a `KeyError` is raised.

### Executing the feed query for a user

1. A caller invokes `VariantQuery.build_for(variant:, user:)`, which assembles the variant config and instantiates a `VariantQuery`.
2. During initialization, the query object calculates the oldest publication date to consider, determines the randomizer seed (from an explicit seed, per-request random, or a cached per-user value), and calls `configure!` to build the JOIN, GROUP BY, and relevance score component lists from the active levers. Levers marked `user_required` are skipped when no user is present.
3. When `call` is invoked, the query constructs a SQL sub-query that selects article IDs and their computed `relevancy_score` (the product of all active lever CASE expressions), then wraps it in a `WITH seeder` CTE to attach a stable `RANDOM()` value to each article.
4. The resulting `ActiveRecord::Relation` joins articles to the sub-query result set, applies the configured ORDER BY, eager-loads comments and reaction categories, and filters out any tags the user has muted.
5. Articles with a score below zero, published outside the recency window (unless recently commented on), or belonging to blocked authors are excluded from the result.

### Configuring a relevancy lever with scoring weights

1. A caller invokes `RelevancyLever#configure_with`, providing a `cases` array of `[range_value, weight]` pairs and a numeric `fallback` weight.
2. The lever validates that `fallback` is a `Numeric` value; if not, it raises `InvalidFallbackError`.
3. The lever validates that `cases` is an array of numeric pairs; if not, it raises `InvalidCasesError`.
4. If the lever declares named query parameters, it extracts and casts each from the provided keyword arguments; missing parameters raise `InvalidQueryParametersError`.
5. On success, the lever returns a `RelevancyLever::Configured` struct containing all resolved values, ready for use in SQL generation.

## Failures / Exceptions

- `LeverCatalogBuilder::DuplicateLeverError` — raised when a relevancy or order-by lever is registered with a key that already exists in the catalog.
- `RelevancyLever::InvalidFallbackError` — raised by `configure_with` when the fallback value is not a `Numeric`.
- `RelevancyLever::InvalidCasesError` — raised by `configure_with` when the cases argument is not an array of numeric pairs.
- `RelevancyLever::InvalidQueryParametersError` — raised by `configure_with` when the provided keyword arguments do not match the lever's declared `query_parameter_names`.
- `KeyError` — raised by `LeverCatalogBuilder#fetch_lever` or `#fetch_order_by` when the requested key is not registered, and by `VariantAssembler#build_with` when the variant JSON references an unregistered lever key.
- `Errno::ENOENT` — raised by `VariantAssembler.call` when the named variant JSON file does not exist in `DIRECTORY`.
