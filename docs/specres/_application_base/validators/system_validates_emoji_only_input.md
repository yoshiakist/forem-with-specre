---
id: "01KJXNEGT06M76HSE5X3EBTZ3V"
name: "system_validates_emoji_only_input"
status: "stable"
last_verified: "2026-03-05"
---

## Related Files

- `app/validators/emoji_only_validator.rb`
- `spec/validators/emoji_only_validator_spec.rb` (Test)

## Functional Overview

`EmojiOnlyValidator` is an `ActiveModel::EachValidator` that ensures a validated attribute contains only emoji characters. When the attribute value is non-nil and non-blank, the validator strips all recognized RGI emoji from the value using `EmojiRegex::RGIEmoji` and checks whether any characters remain. If residual characters exist after stripping, an error is added to the attribute using either a custom message provided via the `options[:message]` key or the default I18n translation at `validators.emoji_only_validator.invalid_emoji`. Nil and empty-string values are allowed through without error to stay compatible with optional fields.

## Scenarios

### Value is nil or empty

1. The attribute value is `nil` or an empty string.
2. The validator returns immediately without adding any error.
3. The record is considered valid for this attribute.

### Value contains only emoji

1. The attribute value consists entirely of one or more RGI emoji characters (e.g., "🍀" or "👍🎉").
2. After stripping all emoji, the remaining string is blank.
3. No error is added and the record is valid.

### Value contains non-emoji characters

1. The attribute value includes at least one character that is not an RGI emoji (e.g., plain text or punctuation).
2. After stripping emoji, one or more characters remain.
3. An error is added to the attribute — using the caller-supplied message if present, otherwise the I18n default.
4. The record is invalid.

### Validation skipped via conditional option

1. The model uses `validates :name, emoji_only: true, if: :some_condition?`.
2. `some_condition?` returns false at validation time.
3. `EmojiOnlyValidator` is never invoked and the attribute value is not checked.
4. The record is valid regardless of what the attribute contains.

## Design Intent

Returning early for `nil` and blank-after-stripping values keeps the validator composable with `presence` and `allow_blank` options applied separately, avoiding redundant error messages.
