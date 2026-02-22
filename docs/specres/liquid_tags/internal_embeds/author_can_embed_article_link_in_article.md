---
id: "01KJ1F417EWY0A879VG771XT85"
name: "author_can_embed_article_link_in_article"
status: "stable"
last_verified: "2026-02-22"
---

## Related Files

- `app/liquid_tags/link_tag.rb`
- `app/views/articles/_liquid.html.erb` (Template)
- `spec/liquid_tags/link_tag_spec.rb` (Test)

## Functional Overview

Authors can embed a rich link preview card for any article on the platform by writing `{% link username/article-slug %}` (or its `{% post %}` alias) in their article body. The tag resolves the referenced article by parsing the given slug or URL, looking up the article first by user username, then by organization slug, and renders an HTML card showing the article title, author (and organization if applicable), publish date, tags, and profile images. If the article does not exist or has been deleted, a "Article No Longer Available" placeholder card is rendered instead.

## Design Intent

The tag accepts multiple input forms (bare slug, path with leading/trailing slashes, full URL including subforem domains) so authors do not need to know the canonical form. Domain validation prevents embedding articles from external sites, while subforem support allows a network of related communities to cross-link freely. The fallback to organization lookup means organization-owned articles are discoverable via either the author username or the organization slug. The `{% post %}` alias is provided for backward compatibility.

## Key Members

- `slug_or_path_or_url` — The raw input provided inside the tag: may be `username/slug`, `/username/slug/`, or a full URL such as `https://example.com/username/slug`.
- `article_hash` — An intermediate `{username:, slug:}` hash extracted from the normalized path, used for both user and organization lookups.
- `PARTIAL` — The Rails partial `articles/liquid` used to render the HTML card, receiving `article` and `title` locals.

## Scenarios

### Embed article by bare slug

1. Author writes `{% link username/article-slug %}` in an article body.
2. The tag strips any surrounding whitespace and HTML entities from the input.
3. The path is parsed; no domain is found, so domain validation is skipped.
4. `{username: "username", slug: "article-slug"}` is extracted from the path.
5. The system looks up a user with that username; a match is found and the user's article with that slug is returned.
6. The rendered card shows the article title, author profile image, author name, publish date, and tags.

### Embed article by path with leading and/or trailing slashes

1. Author writes `{% link /username/article-slug/ %}`.
2. Leading and trailing slashes are stripped before template extraction.
3. Resolution and rendering proceed as in the bare-slug scenario.

### Embed article by full URL on the app domain

1. Author writes `{% link https://app.example.com/username/article-slug %}`.
2. The domain is extracted from the URL and compared against the app domain and all known subforem domains (case-insensitively).
3. The domain matches; path extraction proceeds normally.
4. The article is resolved and the rich card is rendered.

### Embed article published under an organization

1. The slug resolves to an organization slug rather than a user username (user lookup returns nothing).
2. The tag falls back to looking up an organization by the extracted username value.
3. The organization's article with the matching slug is found.
4. The rendered card shows the organization profile image, organization name alongside the individual author name, article title, publish date, and tags.

### Use `{% post %}` alias

1. Author writes `{% post username/article-slug %}` instead of `{% link %}`.
2. The `post` tag is mapped to the same `LinkTag` class and produces identical output.

### Article no longer exists

1. The tag is parsed with a slug that matches no user article and no organization article (e.g., the article was deleted).
2. Both lookup methods return nil; `@article` is nil.
3. The rendered card shows an "Article No Longer Available" placeholder.

## Failures / Exceptions

- If the input contains a domain that is neither the app domain nor any registered subforem domain, a `StandardError` is raised with a localized message indicating the link does not belong to this platform.
- If the path cannot be parsed into a `{username, slug}` pair (e.g., only one path segment), a `StandardError` is raised with a localized message indicating the article does not exist.
- HTML special characters in article titles and organization names are escaped in the rendered output to prevent XSS.
