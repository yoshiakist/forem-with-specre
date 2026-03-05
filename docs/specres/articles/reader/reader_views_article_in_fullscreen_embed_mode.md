---
id: "01KJCKM0HKSQY0DQA3Q8METJ13"
name: "reader_views_article_in_fullscreen_embed_mode"
status: "draft"
---

## Related Files

- `app/controllers/stories_controller.rb`
- `app/views/articles/_fullscreen_embed.html.erb`
- `app/views/articles/show.html.erb`
- `spec/requests/articles/articles_show_spec.rb` (Test)
- `spec/requests/stories_show_spec.rb` (Test)

## Functional Overview

When an article's `type_of` attribute is set to `"fullscreen_embed"`, the article show page bypasses the standard three-column layout and instead renders the `_fullscreen_embed` partial, which takes over the entire browser viewport. The article body fills the content area edge-to-edge while a narrow floating actions sidebar is fixed on the left. Standard inline sections for comments, moderation, and sharing are replaced by a universal modal overlay that loads each section in an iframe when triggered. JavaScript bundles specific to the standard article page are skipped, and the fullscreen embed initialises its own event listeners after a short delay to override any default reaction button behaviour. Only admins and super admins may create articles with `type_of == "fullscreen_embed"`.

## Design Intent

The fullscreen embed mode is designed for articles meant to be displayed inside external sites or consumed as immersive, fullscreen interactive content. By fixing the layout to the viewport and routing secondary interactions (comments, moderation, sharing) through a single modal, the design keeps the primary content permanently visible and avoids the scroll interruption that inline panels would cause. Loading modal content inside iframes also sidesteps character-encoding conflicts between the host page and the embedded section content.

## Scenarios

### Standard fullscreen embed rendering

1. A reader navigates to an article whose `type_of` is `"fullscreen_embed"`.
2. `StoriesController#show` resolves the article and delegates to the `articles/show` template.
3. `show.html.erb` detects `@article.type_of == "fullscreen_embed"` and renders `articles/_fullscreen_embed` instead of the standard three-column layout.
4. The page-level JavaScript bundles (`webShare`, `articlePage`, etc.) are not loaded for this branch.
5. The partial renders a fixed `#article-body` container filling the viewport and a narrow `crayons-layout__sidebar-left` aside holding the actions partial.
6. The article's processed HTML is rendered directly inside `#fullscreen-body`, which occupies the remaining viewport width.
7. On `DOMContentLoaded`, `initializeFullscreenEmbed` runs and binds custom click handlers to the comments, moderation, and "more options" action buttons.

### Reader opens the comments modal

1. The reader clicks the comments action button (`#reaction-butt-comment`) in the floating sidebar.
2. `initializeFullscreenEmbed` intercepts the click, preventing any default reaction behaviour.
3. The universal modal (`#comments-modal`) is made visible with a scale-in animation.
4. An iframe pointing to `{article.path}/comments` is injected into the modal body, loading comments independently.
5. `document.body` overflow is locked to prevent background scrolling while the modal is open.
6. The reader closes the modal by clicking the close button, clicking the backdrop, or pressing Escape; the modal hides and body overflow is restored.

### Reader opens the moderation actions modal

1. A signed-in moderator or admin clicks a moderation button (`.mod-actions-menu-btn`) in the sidebar.
2. The click is intercepted by `initializeFullscreenEmbed`'s handler.
3. The universal modal opens with an iframe pointing to `{article.path}/actions_panel`, loading the moderation panel independently.
4. The modal can be dismissed the same way as the comments modal.

### Reader opens the "More Options" modal (sharing and extra actions)

1. The reader clicks the "More Options" button (`#article-show-more-button`) in the actions sidebar.
2. `initializeFullscreenEmbed` intercepts the click.
3. The universal modal opens with the pre-rendered HTML from the hidden `#extra-menu-content` container, which includes social sharing links (Twitter, LinkedIn, Facebook, Mastodon), the Web Share API entry point, copy-link functionality, and a report-abuse link.
4. Clicking "Copy link" uses `navigator.clipboard.writeText` and shows a success announcer for three seconds.
5. The modal is dismissed by the same three mechanisms as the comments modal.

## Failures / Exceptions

- If modal DOM elements are missing when `initializeFullscreenEmbed` runs, an error is logged to the console and the modal interaction is silently skipped; no fallback UI is shown.
- On mobile viewports (max-width 767 px), the actions sidebar collapses to a narrow strip and the main content area adjusts to leave room for a bottom actions bar.
- Viewport height is recomputed on `resize` and `orientationchange` to handle mobile browser chrome changes; layout relies on the `--vh` CSS custom property.
- When the platform navigation sidebar (`data-side-nav-visible="true"`) is toggled, a `MutationObserver` forces a reflow so the fixed-position elements realign correctly.
