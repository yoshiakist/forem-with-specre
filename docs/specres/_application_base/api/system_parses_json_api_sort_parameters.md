---
id: "01KJXS65QNM2GD19RTCWHQ5RCC"
name: "system_parses_json_api_sort_parameters"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/controllers/concerns/json_api_sort_param.rb`
- `spec/controllers/concerns/json_api_sort_param_spec.rb` (Test)

## Functional Overview

The `JsonApiSortParam` concern provides controllers with a `parse_sort_param` method that translates JSON API style sort query strings into an ordered hash of field-to-direction pairs. It accepts a comma-separated sort string (e.g., `"created_at,-updated_at"`), where a leading minus sign denotes descending order and no prefix denotes ascending order. The result is filtered to only include fields from an allowed list, and the output order follows the order of the allowed fields list rather than the input order. If the parsed result is empty (due to an empty string or all fields being filtered out), a caller-supplied default sort order is returned instead.

## Design Intent

The concern enforces a JSON API-compliant sort parameter convention. Filtering by an allowed-fields list prevents callers from sorting on arbitrary columns, protecting against performance and security issues. Preserving the order defined by `allowed_fields` (rather than the input order) gives the controller explicit control over sort precedence across all requests.

## Key Members

- `parse_sort_param(param_string, allowed_fields:, default_sort:)` — public entry point; `param_string` defaults to `params[:sort]`; `allowed_fields` is an array of symbols defining permitted sort columns; `default_sort` is a hash used when the parsed result is empty
- `fields_to_hash(fields)` — private; converts an array of raw field strings into a symbol-keyed hash of `:asc` / `:desc` values
- `sort_and_filter(fields_hash, allowed_fields)` — private; removes disallowed keys and reorders the remaining entries to match the position of each field in `allowed_fields`

## Scenarios

### Default parameter source

1. A controller includes `JsonApiSortParam` and receives a request with a `sort` query parameter.
2. The caller invokes `parse_sort_param` without an explicit first argument.
3. The concern reads `params[:sort]` automatically and returns the parsed sort hash.

### Ascending and descending field parsing

1. A caller passes a comma-separated sort string such as `"created_at,-updated_at"` along with an allowed-fields list containing both fields.
2. The concern splits the string on commas and inspects each token for a leading minus sign.
3. Fields without a minus are mapped to `:asc`; fields with a minus (stripped) are mapped to `:desc`.
4. The resulting hash is returned with each allowed field mapped to its direction.

### Output order follows allowed_fields, not input order

1. A caller passes a sort string where the fields appear in a different order than in `allowed_fields`.
2. After parsing and filtering, the concern reorders the result to match the sequence declared in `allowed_fields`.
3. The returned hash preserves the allowed-fields order regardless of input order.

### Filtering disallowed fields

1. A caller passes a sort string that includes a field not present in `allowed_fields`.
2. The concern discards any field not in the allowed list.
3. The returned hash contains only the intersection of requested fields and allowed fields.

### Fallback to default sort

1. A caller passes an empty string, a nil value, or a string whose fields are all disallowed.
2. After parsing and filtering, the result is empty.
3. The concern returns the `default_sort` hash provided by the caller unchanged.
