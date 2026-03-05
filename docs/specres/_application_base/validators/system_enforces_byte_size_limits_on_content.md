---
id: "01KJXNBTX3Q3NFRF9BJJ18Z149"
name: "system_enforces_byte_size_limits_on_content"
status: "draft"
---

## Related Files

- `app/validators/bytesize_validator.rb`

## Functional Overview

`BytesizeValidator` is a custom `ActiveModel::EachValidator` that enforces a maximum byte size on a model attribute. Unlike Rails' built-in length validator, which counts characters, this validator measures the raw byte count of a value — ensuring that multi-byte characters (such as emoji or non-ASCII text) are correctly bounded. It currently supports only the `:maximum` option. When the byte size of the attribute value exceeds the configured maximum, the validator adds a `:too_long` error to the record with the limit count available for interpolation in the error message.

## Design Intent

Rails' built-in `LengthValidator` counts characters, not bytes. For fields backed by database columns with byte-length constraints (e.g., `VARCHAR(255)` in byte-mode databases), a character-count validator can allow strings that overflow the column. This validator was adapted from a known Rails issue to close that gap precisely.

## Key Members

- `MESSAGES` — maps the `:maximum` check key to the `:too_long` i18n error key
- `CHECKS` — maps the `:maximum` check key to the `<=` comparison operator
- `RESERVED_OPTIONS` — option keys that are consumed internally and must not be forwarded to `errors.add`

## Scenarios

### Configuration is valid

1. A model declares `validates :body, bytesize: { maximum: 65_535 }` with a non-negative integer limit.
2. `BytesizeValidator#check_validity!` confirms the `:maximum` key is present and its value is a non-negative integer.
3. Validation setup proceeds without error.

### Attribute value is within the byte limit

1. A record is validated and the attribute holds a string whose byte size is less than or equal to the configured maximum.
2. `BytesizeValidator#validate_each` computes the byte size, compares it against the maximum, and finds it within bounds.
3. No error is added to the record; the record remains valid.

### Attribute value exceeds the byte limit

1. A record is validated and the attribute holds a string whose byte size exceeds the configured maximum (e.g., a string containing multi-byte emoji characters).
2. `BytesizeValidator#validate_each` computes the byte size and determines it is greater than the maximum.
3. The validator adds a `:too_long` error to the attribute, including the maximum byte count as `:count` for message interpolation.
4. A custom `:too_long` message, if provided in the validator options, is applied to the error.

### Value does not respond to `bytesize`

1. A record is validated and the attribute holds a non-string value that does not implement `bytesize`.
2. The validator falls back to calling `.to_s.bytesize` on the value before performing the comparison.
3. Validation proceeds as normal against the resulting byte count.

## Failures / Exceptions

- If the validator is configured without a `:maximum` option, `check_validity!` raises `ArgumentError` (using `ERROR_MESSAGE`).
- If the `:maximum` option is not a non-negative integer, `check_validity!` raises `ArgumentError` with an i18n message from `validators.bytesize_validator.non_negative`.
