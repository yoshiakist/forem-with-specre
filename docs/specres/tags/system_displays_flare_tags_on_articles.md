---
id: "01KJ41JJ73MXNDK5F9W99N0P0A"
name: "system_displays_flare_tags_on_articles"
status: "stable"
last_verified: "2026-02-23"
---

## Related Files

- `app/services/flare_tag.rb`
- `app/services/homepage/fetch_tag_flares.rb`
- `app/javascript/articles/components/TagList.jsx`
- `app/views/articles/_tag_identifier.html.erb` (Template)
- `spec/services/flare_tag_spec.rb` (Test)
- `spec/services/homepage/fetch_tag_flares_spec.rb` (Test)

## Functional Overview

The system identifies a single "flare tag" for each article from a predefined set of special tag names (`Constants::Tags::FLARE_TAG_NAMES`) and displays it with custom brand colors distinct from ordinary tags. `FlareTag` resolves the flare tag for a single article by intersecting its cached tag list with the known flare tag set, optionally excluding one tag by name. `Homepage::FetchTagFlares` performs the same resolution in bulk for a collection of articles, returning a map of article IDs to flare tag attribute hashes. The `TagList` frontend component renders the flare tag first with filled styling and custom CSS color variables, then renders remaining tags with the flare tag filtered out. The `_tag_identifier` template applies the same single-article lookup to render an inline colored badge next to the article title.

## Design Intent

Flare tags are a curated, fixed set of special community tags (e.g., "ama", "explainlikeimfive") that deserve visual prominence. Rather than styling every tag equally, the system elevates exactly one flare tag per article. The `except_tag` parameter on `FlareTag` allows tag-index pages to suppress the current page's own tag from appearing as a flare badge, avoiding redundant display. The bulk `FetchTagFlares.call` path avoids N+1 queries by computing all flare assignments from a plucked tag list before issuing a single `Tag.where` lookup.

## Key Members

- `FlareTag::FLARE_TAG_IDS_HASH` — frozen hash mapping each known flare tag name to its database ID, built at class load time to avoid repeated queries.
- `flare_tag` (in `TagList`) — object with `name`, `bg_color_hex`, and `text_color_hex` fields passed as a prop; its presence determines whether the filled flare badge is rendered.
- `ATTRIBUTES` (in `FetchTagFlares`) — the three tag fields (`name`, `bg_color_hex`, `text_color_hex`) fetched and serialized for every flare match.

## Scenarios

### Article has a recognized flare tag

1. An article's cached tag list contains at least one name present in `Constants::Tags::FLARE_TAG_NAMES`.
2. `FlareTag#tag` finds the first matching tag ID from `FLARE_TAG_IDS_HASH` and loads its name and color fields from the database.
3. The template renders a colored inline badge before the article title; the `TagList` component renders the flare tag as a filled, color-styled link and omits it from the plain tag list beneath.

### Article has no recognized flare tag

1. An article's cached tag list contains no name present in `Constants::Tags::FLARE_TAG_NAMES`, or the tag list is blank.
2. `FlareTag#tag` returns nil; `FetchTagFlares` skips the article when building the flare map.
3. No flare badge is rendered; the `TagList` component displays all tags as ordinary links.

### Flare tag is suppressed for the current tag page

1. A tag index page calls `FlareTag.new(article, current_tag_name)` where `current_tag_name` matches the article's flare tag.
2. The `except_tag` check causes `tag_id` to return nil even though the tag is in the flare set.
3. No flare badge is shown for that article on the current tag's page.

### Bulk resolution for a homepage article feed

1. A list of articles is passed to `Homepage::FetchTagFlares.call`.
2. The service plucks each article's id and cached tag list, finds the intersection with `FLARE_TAG_NAMES`, and groups article IDs by their matched flare tag name.
3. A single `Tag.where` query loads color attributes for all matched flare tag names.
4. The method returns a hash keyed by article ID, each value being a JSON-serializable hash of `name`, `bg_color_hex`, and `text_color_hex`.

### Article has multiple flare tags

1. An article's cached tag list contains more than one name from `Constants::Tags::FLARE_TAG_NAMES`.
2. `FlareTag` takes the first match found in `FLARE_TAG_IDS_HASH`; `FetchTagFlares` takes the first intersection result from the set operation.
3. Only one flare tag is displayed per article regardless of how many flare-eligible tags it carries.

## Failures / Exceptions

- If `cached_tag_list` is nil or blank, `FetchTagFlares` skips the article with a `next` guard, returning no flare entry for it.
- If the flare tag name is found in `FLARE_TAG_IDS_HASH` but the corresponding `Tag` record no longer exists in the database, `FlareTag#tag` returns nil and no badge is rendered.
