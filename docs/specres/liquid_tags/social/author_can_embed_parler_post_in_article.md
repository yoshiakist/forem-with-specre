---
id: "01KJ1FKTVQH3HSYPJR6QFEWZ94"
name: "author_can_embed_parler_post_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/parler_tag.rb`
- `app/views/liquids/_parler.html.erb` (Template)
- `spec/liquid_tags/parler_tag_spec.rb` (Test)

## Functional Overview

An article author can embed a Parler audio post by using the `{% parler <url> %}` Liquid tag in their article body. The tag accepts a valid Parler audio URL, validates its format, and renders an iframe pointing to the Parler player API. If the URL does not match the expected Parler audio format, the tag raises an error and the embed is rejected.

## Design Intent

The URL is the canonical identifier for a Parler audio post rather than a short numeric ID, so the tag validates the full URL to ensure it points to a genuine Parler audio resource. Width and height are fixed constants baked into the partial to provide a consistent visual presentation across all articles without requiring author configuration.

## Key Members

- `PARTIAL` — Path to the ERB template (`liquids/parler`) used to render the embed iframe.
- `@id` — The validated Parler audio URL extracted from the tag input.
- `height: 120, width: 710` — Fixed pixel dimensions passed as locals to the partial.
- Valid URL pattern — Must match `https://www.parler.io/audio/<numeric_id>/<hash>.<uuid>.mp3`.

## Scenarios

### Successful embed with a valid Parler URL

1. The author writes `{% parler https://www.parler.io/audio/73240183203/d53cff009eac2ab1bc9dd8821a638823c39cbcea.7dd28611-b7fc-4cf8-9977-b6e3aaf644a1.mp3 %}` in an article.
2. The tag strips any surrounding whitespace from the input and extracts the URL.
3. The URL is validated against the Parler audio URL pattern.
4. The tag renders an iframe with `src` set to `https://api.parler.io/ss/player?url=<url>`, width 710, and height 120.
5. The rendered HTML is embedded in the article body.

### Rejection of an invalid URL

1. The author provides a URL that does not match the Parler audio format (e.g., `https://www.google.com`).
2. The tag attempts to extract and validate the URL.
3. Validation fails and the tag raises a `StandardError` with the message from `liquid_tags.parler_tag.invalid_parler_url`.
4. The article is not saved with the invalid embed.

## Failures / Exceptions

- Any URL that does not match `https://www.parler.io/audio/<1-11 digits>/<11-40 alphanumeric chars>.<11-36 alphanumeric/hyphen chars>.mp3` is rejected with an error.
- Leading or trailing spaces around the URL are tolerated and stripped before validation.
