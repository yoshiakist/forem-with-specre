---
id: "01KJCKF1AY5288JYRWJXK8QQ8C"
name: "system_outputs_article_structured_data_and_meta_tags"
status: "stable"
last_verified: "2026-02-26"
---

## Related Files

- `app/controllers/stories_controller.rb`
- `app/decorators/article_decorator.rb`
- `app/helpers/articles_helper.rb`
- `app/views/articles/show.html.erb`
- `spec/requests/articles/articles_show_spec.rb` (Test)
- `spec/requests/stories_show_spec.rb` (Test)
- `spec/decorators/article_decorator_spec.rb` (Test)
- `spec/helpers/articles_helper_spec.rb` (Test)

## Functional Overview

When a visitor loads an article show page, the system generates a suite of machine-readable metadata and structured data in the rendered HTML. A `<script type="application/ld+json">` tag in the page head contains a Schema.org `Article` object — including author (`Person`), publisher (`Organization` with logo), headline, SEO-optimized images at three aspect ratios, and publication/modification dates. When the article has comments, the JSON-LD is extended with a nested `DiscussionForumPosting` and `Comment` objects (with nested replies) to support Google's rich-results display. In parallel, Open Graph meta tags (`og:type`, `og:url`, `og:title`, `og:description`, `og:image`) and Twitter Card meta tags (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`) are written into the page head for social sharing previews. A canonical URL is always emitted; articles with a low score or other indexability concerns receive `noindex`/`nofollow` `robots` directives. When an article was crossposted from an external platform, the helper `should_show_crossposted_on?` gates display of the original source attribution in the article body. The JSON-LD block is suppressed for signed-in users and for internal (InstantClick) navigation requests.

## Design Intent

The three-size image array in `seo_optimized_images` (1080×1080, 1280×720, 1600×900) follows Google's Article structured-data guidelines, which recommend providing multiple image crops to maximise eligibility for different rich-result formats. Generating structured data server-side and gating it to anonymous, non-internal-navigation requests avoids serving it to crawlers that would land on a signed-in session and keeps it out of InstantClick partial responses (where the `<head>` is not re-evaluated). Embedding `DiscussionForumPosting` and `Comment` objects only when comments are present keeps the JSON-LD payload minimal for articles without discussion activity.

## Scenarios

### Standard published article

1. A visitor (not signed in) requests the article show page via a full browser navigation.
2. The controller calls `set_article_json_ld`, which builds an `Article` JSON-LD object containing the article URL, publisher organization with logo, headline, author Person, `datePublished`, `dateModified`, and an array of three SEO-optimized image URLs.
3. The view renders the JSON-LD inside a `<script type="application/ld+json">` tag in the page head.
4. Open Graph meta tags (`og:type=article`, `og:url`, `og:title`, `og:description`, `og:image`, `og:site_name`) and Twitter Card meta tags (`twitter:card=summary_large_image`, `twitter:title`, `twitter:description`, `twitter:image`) are written into the page head.
5. A `<link rel="canonical">` tag is emitted pointing to the article's canonical URL (if set) or its default app URL.

### Article with comments (DiscussionForumPosting and Comment structured data)

1. The article has one or more published comments (`comments_count > 0`).
2. `build_article_json_ld` detects the positive comment count and appends a `DiscussionForumPosting` object as `mainEntity`, including `headline`, `text`, author `Person`, dates, URL, and `interactionStatistic` counters for comment and like actions.
3. `fetch_comments_for_json_ld` fetches up to 10 top-level comments ordered by score (excluding negative-score comments) via `Comments::Tree`.
4. Each top-level comment is serialised as a `Comment` object with `@id`, `text`, `author`, `datePublished`, `dateModified`, `url`, and `interactionStatistic`.
5. Replies nested under a root comment are included as a `comment` array on the parent `Comment` object; each reply carries a `parentItem` reference linking back to the parent comment's `@id`.
6. The assembled comment array is attached to `mainEntity[:comment]` in the JSON-LD output.

### Crossposted article

1. An article was imported from an external feed (`published_from_feed: true`, `crossposted_at` set, `feed_source_url` present) or has an explicit `canonical_url`.
2. The helper `should_show_crossposted_on?` returns truthy.
3. The article body view renders a crosspost attribution notice displaying the source platform's hostname (formatted by `get_host_without_www`, which strips `www.`, lowercases, and maps `medium.com` to `"Medium"`).
4. The canonical URL meta tag points to the original source URL.

### Article with noindex (low score or other skip-indexing condition)

1. The article's `skip_indexing?` predicate returns true (e.g. score below threshold).
2. The view emits two additional `<meta name="robots">` tags: one with `noindex` and one with `nofollow`.
3. The article is still accessible to human visitors; only search engine crawlers are instructed to skip indexing.

### Internal navigation or signed-in user (JSON-LD suppressed)

1. A signed-in user requests the article page, or any user arrives via an InstantClick internal navigation (indicated by the `?i=i` parameter / `internal_navigation?` helper).
2. The `<script type="application/ld+json">` block is not rendered (the view guards it with `unless internal_navigation? || user_signed_in?`).
3. Open Graph and Twitter Card meta tags are also suppressed in this path because they are written inside the `content_for :page_meta` block, which is only populated in the non-internal-navigation branch.
4. In the internal-navigation branch, the canonical URL and description meta tags are still written directly into the response body (rather than the head) to support InstantClick partial updates.

## Failures / Exceptions

- If `seo_optimized_images` is called for an article with no cover or social image, it still returns the three URLs (pointing to the default social image generator), so the JSON-LD `image` array is always populated for published articles.
- If an article has comments but none pass the `Comments::Tree` filter (e.g. all are negatively scored), `fetch_comments_for_json_ld` returns an empty array and the `comment` key is omitted from `mainEntity`, leaving only the `DiscussionForumPosting` wrapper.
- `build_comment_json_ld` uses safe navigation (`comment&.user&.name`) to tolerate deleted-user comments without raising.
- The JSON-LD is only rendered for non-signed-in, non-internal-navigation requests; if a search engine crawler somehow arrives as a signed-in session, structured data will be absent.
