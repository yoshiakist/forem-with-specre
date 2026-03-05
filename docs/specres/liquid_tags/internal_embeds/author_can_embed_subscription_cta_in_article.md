---
id: "01KJ1F6M9DTXAJNC4ZQFMSWJXE"
name: "author_can_embed_subscription_cta_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/user_subscription_tag.rb`
- `app/models/liquid_tags/user_subscription_tag.rb`
- `app/models/user_subscription.rb`
- `app/views/liquids/_user_subscription.html.erb` (Template)
- `spec/liquid_tags/user_subscription_tag_spec.rb` (Test)

## Functional Overview

An author can embed a `{% user_subscription %}` liquid tag inside an article body to render a subscription call-to-action (CTA) widget. The tag accepts a single argument — the CTA text — and renders an HTML partial that displays the author's profile image, the custom CTA text, and a subscription button. The widget adapts to the reader's authentication state: signed-out readers see a prompt to sign in, signed-in readers see a subscribe button, and readers using Apple private-relay email see a disabled button with an explanatory message. Authorization to use the tag is controlled by Rolify roles, restricting access to admins, super-admins, and users explicitly granted the `restricted_liquid_tag` role for `LiquidTags::UserSubscriptionTag`.

## Design Intent

The tag is deliberately narrow: it only works inside `Article` contexts (`VALID_CONTEXTS`). This prevents the widget from appearing in places (e.g., comments) where subscription semantics are unclear or undesirable.

Authorization is delegated to `user_subscription_tag_available?` via `LiquidTagBase.user_authorization_method_name`, following the same per-tag role-checking pattern used by other restricted liquid tags. `LiquidTags::UserSubscriptionTag` is a Rolify-backed model class (with no database table) purely to serve as the resource argument to `has_role?`, keeping role management consistent across all restricted tags.

The `UserSubscription` model enforces integrity rules that complement the tag: a subscription record is only valid when the source article actually contains the tag in its body, the source is published, and the subscriber did not sign up via Apple private-relay email. This means the tag and the model together define the full contract for subscription creation.

## Key Members

- `PARTIAL` — path `"liquids/user_subscription"` pointing to the ERB partial that renders the widget
- `VALID_CONTEXTS` — `["Article"]`; the tag raises an error if used outside this context
- `VALID_ROLES` — `:admin`, `[:restricted_liquid_tag, LiquidTags::UserSubscriptionTag]`, `:super_admin`
- `cta_text` — the raw string argument passed to the tag; stripped of leading/trailing whitespace and forwarded to the partial as-is
- `author_profile_image` — 90px profile image URL of the article author, passed to the partial
- `author_username` — username of the article author, passed to the partial and used as the `data-author-username` attribute on the widget root element
- `community_name` — retrieved from `Settings::Community.community_name` and passed to the partial for display in subscription-related copy

## Scenarios

### Author embeds the tag with custom CTA text

1. Author writes `{% user_subscription Some sweet CTA text %}` in an article body.
2. The liquid tag is parsed; `UserSubscriptionTag#initialize` stores the stripped CTA text, the article as the source, and the author as the user.
3. On render, the partial receives the CTA text, the author's 90px profile image URL, the author's username, and the community name.
4. The rendered HTML includes the CTA text, the author's username, and the author's profile image.

### Signed-out reader views the widget

1. A reader who is not authenticated loads an article containing the tag.
2. The widget displays the `.ltag__user-subscription-tag__signed-out` section with a prompt referencing the community name and a "Sign in" link pointing to `/enter`.
3. The signed-in and Apple-auth sections remain hidden.

### Signed-in reader subscribes

1. A signed-in reader views the widget; the JavaScript layer shows the `.ltag__user-subscription-tag__signed-in` section.
2. The reader clicks the subscribe button.
3. A confirmation modal is shown, identifying the author by username.
4. The reader confirms; the client submits a subscription request.
5. On success, a response message is displayed in the `.ltag__user-subscription-tag__response-message` area.

### Reader with Apple private-relay email views the widget

1. A signed-in reader whose email ends with `@privaterelay.appleid.com` views the widget.
2. The JavaScript layer shows the `.ltag__user-subscription-tag__apple-auth` section.
3. The subscribe button is rendered in a disabled state with a message explaining that the community email cannot be updated.

### Unauthorized user attempts to use the tag

1. A user without `:admin`, `:super_admin`, or the `restricted_liquid_tag` role for `LiquidTags::UserSubscriptionTag` attempts to render the tag.
2. `user_subscription_tag_available?` returns false and the tag is not rendered.

## Failures / Exceptions

- If the article body does not contain the `{% user_subscription %}` tag, `UserSubscription#tag_enabled` validation fails with a "not enabled" error, preventing subscription records from being created.
- If the subscription source (article) is unpublished, `UserSubscription#active_user_subscription_source` validation fails, blocking new subscriptions.
- If the subscriber's email ends with `@privaterelay.appleid.com`, `UserSubscription#non_apple_auth_subscriber` validation fails, blocking record creation.
- If `MarkdownProcessor::Parser` raises any error while parsing the article body to detect tags used, the `liquid_tags_used` method rescues with an empty array, causing `tag_enabled` to add a validation error rather than crash.
- The tag is only valid inside `Article` contexts; use in other contexts (e.g., comments) is rejected by `VALID_CONTEXTS`.
