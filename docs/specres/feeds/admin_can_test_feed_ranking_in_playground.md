---
id: "01KJ24JR0FK5MWHWK01QF0434H"
name: "admin_can_test_feed_ranking_in_playground"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/controllers/admin/tools_controller.rb`
- `app/views/admin/tools/feed_playground.html.erb` (Template)
- `spec/requests/admin/feed_playground_spec.rb` (Test)

## Functional Overview

The feed playground allows admins to interactively test feed ranking configurations without affecting production. An admin submits a JSON configuration and an optional username, and the system assembles a variant feed using `Articles::Feeds::VariantAssembler` and `Articles::Feeds::VariantQuery` to produce a ranked article preview. If no configuration is submitted, the page renders an empty form. Errors in the JSON or the query (such as invalid JSON or a database error) are captured and surfaced as a flash message rather than raising an unhandled exception.

## Design Intent

The playground is intentionally read-only and stateless — it does not persist any configuration. This lets admins experiment with feed-ranking levers safely. Falling back to `current_user` when the given username is not found keeps the tool usable even when a username is mistyped.

## Key Members

- `config` param — raw JSON string describing the feed variant configuration
- `username` param — optional username to simulate the feed for; falls back to the currently signed-in admin
- `number_of_articles` param — how many articles to include in the preview; defaults to 25
- `@feed` — a `Articles::Feeds::VariantQuery` instance built from the parsed configuration
- `@articles` — the ordered article list produced by calling `more_comments_minimal_weight_randomized` on the feed query

## Scenarios

### Admin views the empty playground form

1. An admin navigates to the feed playground page without submitting any parameters.
2. The system detects that `config` is blank and returns early, rendering the form with no results.
3. The page displays a textarea for the JSON configuration, a username field pre-filled with the current admin's username, and a number-of-articles field defaulting to 25.

### Admin submits a valid feed configuration

1. The admin fills in a valid JSON configuration, optionally specifies a username, and submits the form.
2. The system parses the JSON and assembles a feed variant using `Articles::Feeds::VariantAssembler` with the lever catalog.
3. If the username resolves to an existing user, that user is used; otherwise the current admin is used.
4. `Articles::Feeds::VariantQuery` executes the ranking query and returns an ordered list of articles.
5. The template renders the user's followed-tag weights and the ranked article list beneath the form.

### Admin submits an invalid or malformed JSON configuration

1. The admin submits a configuration string that is not valid JSON, or that references an unknown feed lever key.
2. The system rescues `JSON::ParserError` or `KeyError` (and `ActiveRecord::StatementInvalid` for query failures) and stores the error message in the flash.
3. The page re-renders with the flash danger message visible and no article results.

### Non-admin user attempts to access the playground

1. A regular user (or a single-resource admin without `Tool` resource access) requests the feed playground endpoint.
2. The system raises `Pundit::NotAuthorizedError`, blocking the request.

## Failures / Exceptions

- `JSON::ParserError` — raised when the `config` param is not valid JSON; message is shown in the flash.
- `KeyError` — raised when the JSON references an unrecognized lever; message is shown in the flash.
- `ActiveRecord::StatementInvalid` — raised when the generated query is invalid; message is shown in the flash.
- `Pundit::NotAuthorizedError` — raised by the authorization layer when the requester is not an admin with tool access.
