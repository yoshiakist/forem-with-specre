---
id: "01KJCKAY2FQDDK8VYRS35EC42E"
name: "reader_navigates_article_series"
status: "draft"
---

## Related Files

- `app/controllers/stories_controller.rb`
- `app/views/articles/_collection.html.erb`
- `app/views/articles/show.html.erb`
- `spec/system/collections/user_views_collection_articles_spec.rb` (Test)

## Functional Overview

When an article belongs to a collection (series), the article show page renders a series navigation widget that lists all published articles in the series in chronological order, highlights the currently viewed article, and collapses middle entries into a "Show X more" toggle when the series contains more than five articles. The controller's `assign_article_show_variables` loads the collection and its published articles ordered by original publication date (using `crossposted_at` when available). The `_collection.html.erb` partial renders the widget, and `show.html.erb` renders it a second time below the article body when the article is long.

## Design Intent

Cross-posted articles may have a `crossposted_at` date earlier than `published_at`, so the ordering uses `COALESCE(crossposted_at, published_at)` to place them correctly within the series. Only published articles from the current subforem are included, keeping the widget consistent with what readers can actually access. The collapsing behaviour keeps the widget compact for long series without hiding the first two and last two entries, which are the most contextually relevant.

## Scenarios

### Reader views a series article with 5 or fewer parts

1. A reader navigates to an article that belongs to a collection.
2. The system loads the collection and its published articles ordered by original publication date.
3. The series widget is rendered above the article body, showing "Part X of N" heading with every article title as a link.
4. The currently viewed article's link is marked as active (highlighted).
5. All article titles are visible without any collapsed section.

### Reader views a series article with more than 5 parts

1. A reader navigates to an article that belongs to a collection with six or more published articles.
2. The system loads all published articles in the series.
3. The series widget renders the first two and last two entries as normal links, and inserts a single collapsed "Show X more" toggle in the middle for all entries between position 3 and the third-from-last.
4. If the currently viewed article is one of the collapsed middle entries, the toggle link receives the active style.
5. The reader can expand the collapsed section via the JS-driven toggle.

### Repeat widget for long articles

1. A reader navigates to a long article (determined by body length via `long_markdown?`) that belongs to a collection.
2. The series widget is rendered above the article body as normal.
3. After the article body, the series widget is rendered a second time so the reader can navigate without scrolling back to the top.

### No widget rendered for uncollected articles

1. A reader navigates to an article that does not belong to any collection.
2. The controller sets no `@collection` or `@collection_articles` instance variables.
3. The series widget is not rendered anywhere on the page.

## Failures / Exceptions

- If a collection exists but contains only one published article, the widget is suppressed (`collection_size > 1` guard in the partial).
- Articles that are unpublished or belong to a different subforem are excluded from `@collection_articles` and do not appear in the widget.
