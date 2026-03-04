---
id: "01KJV72NZBF1FK1XSC1ET596PS"
name: "system_renders_article_feed_card"
status: "stable"
last_verified: "2026-03-04"
---

## Related Files

- `app/javascript/articles/Article.jsx`
- `app/javascript/articles/components/ArticleCoverImage.jsx`
- `app/javascript/articles/components/ContentTitle.jsx`
- `app/javascript/articles/components/Meta.jsx`
- `app/javascript/articles/components/PublishDate.jsx`
- `app/javascript/articles/components/ReadingTime.jsx`
- `app/javascript/articles/components/CommentsCount.jsx`
- `app/javascript/articles/components/CommentListItem.jsx`
- `app/javascript/articles/components/CommentsList.jsx`
- `app/javascript/articles/components/SaveButton.jsx`
- `app/javascript/articles/components/index.js`
- `app/javascript/articles/LoadingArticle.jsx`
- `app/javascript/articles/Feed.jsx`
- `app/javascript/articles/components/ReactionsCount.jsx`
- `app/javascript/articles/components/SearchSnippet.jsx`
- `app/javascript/articles/components/TagList.jsx`
- `app/javascript/articles/components/Video.jsx`
- `app/javascript/common-prop-types/article-prop-types.js`
- `app/assets/javascripts/utilities/buildArticleHTML.js`
- `app/assets/javascripts/utilities/getImageForLink.js`
- `app/views/articles/_single_story.html.erb`
- `app/views/articles/_widget_list_item.html.erb`
- `app/javascript/articles/__tests__/Article.test.jsx` (Test)
- `app/javascript/articles/__tests__/ArticleLoading.test.jsx` (Test)
- `app/javascript/articles/components/__tests__/CommentsList.test.jsx` (Test)
- `app/javascript/articles/components/__tests__/SaveButton.test.jsx` (Test)

## Functional Overview

The system renders a feed card for each article (or article-like content) in the home feed, search results, and tag pages. The `Article` component acts as the top-level orchestrator: it decides which sub-components to display based on the article's `class_name`, `type_of`, and contextual flags such as `isFeatured`, `feedStyle`, and `pinned`. A cover image appears for featured articles, rich-feed articles with a main image, or pinned articles that have an image. The `Meta` component shows the author avatar, optional organization logo, and publish date with a time-ago indicator. `ContentTitle` renders the article title with a type badge for podcast episodes and user profiles. `TagList` displays associated tags, `ReactionsCount` and `CommentsCount` show engagement numbers as interactive links, `ReadingTime` shows estimated reading duration, and `SaveButton` lets authenticated users bookmark the article. When the article has top comments, `CommentsList` renders up to two of them with a "See all comments" link when additional comments exist. `LoadingArticle` provides a skeleton placeholder shown while articles are loading. `buildArticleHTML` is a legacy plain-JS function that generates equivalent card HTML server-side or outside the Preact render tree. The ERB partials `_single_story` and `_widget_list_item` serve the same card structure from Rails views.

## Key Members

- `isFeatured: bool` — when true, adds the `crayons-story--featured` class and makes the cover image visible
- `feedStyle: string` — `"rich"` enables cover image display for non-featured articles that have a `main_image`
- `pinned: bool` — shows a pin badge and allows the cover image even when the article is not featured
- `saveable: bool` — controls whether the bookmark button is rendered at all
- `isBookmarked: bool` — initial bookmark state; `SaveButton` maintains local toggle state after mount
- `numberOfCommentsToShow` (CommentsList) — constant set to 2; limits the inline comment previews

## Scenarios

### Standard article card

1. The feed receives an article object with `class_name` of `Article`.
2. The system renders an `<article>` element with the `crayons-story` class, an accessible hidden navigation link, author meta (avatar, name, publish date), the article title, tags, reactions count, comments count, reading time, and a bookmark button.
3. Clicking any part of the card body navigates to the article URL using InstantClick; middle-click or Ctrl/Cmd-click opens it in a new tab.

### Featured article with cover image

1. An article is rendered with `isFeatured` set to true and a `main_image` present, and the article has no video.
2. The system adds the `crayons-story--featured` class to the card and renders the `ArticleCoverImage` component above the body, preserving the image's aspect ratio via inline style.
3. The card is otherwise identical to a standard card.

### Article with top comments preview

1. An article has a non-empty `top_comments` array.
2. The system renders a `CommentsList` section beneath the card body showing at most two comments, each displaying the commenter avatar, name, timestamp, and a truncated version of the comment body.
3. When the total `comments_count` exceeds two, a "See all N comments" button links to the article's comments section.

### Loading skeleton state

1. The feed is awaiting article data from the server.
2. The system renders `LoadingArticle` components in place of real cards; each skeleton contains grey scaffold blocks for the avatar, author line, and title area.
3. For the featured slot the skeleton also includes a cover image placeholder with a fixed aspect ratio.

### Save / bookmark toggle

1. A reader views an article card and the article's `class_name` is `Article` and `saveable` is true.
2. The `SaveButton` renders with a bookmark icon reflecting the current `isBookmarked` state (`aria-pressed` attribute set accordingly).
3. When the reader clicks the button, the component toggles its local bookmarked state and calls the `onClick` handler (which triggers the API request in the parent); the icon switches between the outlined and filled bookmark SVG.

## Failures / Exceptions

- When `article.type_of` is `"podcast_episodes"`, `Article` delegates rendering to `PodcastArticle` instead of the standard card layout.
- `CommentsCount` renders null when `count` is neither 0 nor a positive number (i.e., undefined).
- `SaveButton` renders null when `class_name` is neither `"Article"` nor `"User"`.
- `CommentsList` renders nothing (empty string) when the `comments` prop is absent or an empty array.
- `Meta` returns an empty string when the article title is `"[Boost]"`, suppressing the author block for boosted posts.
- `ContentTitle` renders a special "Boosted by" span when the article title is `"[Boost]"`.
