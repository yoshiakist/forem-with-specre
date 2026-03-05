---
id: "01KJ6C1WBXTZN9GA5WYQPMQJSA"
name: "user_views_articles_in_collection"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/controllers/collections_controller.rb`
- `app/models/collection.rb`
- `app/views/collections/show.html.erb` (Template)
- `app/views/collections/_meta.html.erb` (Template)
- `spec/requests/collections_spec.rb` (Test)
- `spec/system/collections/user_views_collection_articles_spec.rb` (Test)
- `spec/factories/collections.rb` (Test)

## Functional Overview

When a user navigates to a collection's show page, the system loads the collection by its ID, retrieves all published articles belonging to that collection that are from the current subforem, and renders them in chronological order based on their publication date (falling back to crosspost date). The page displays the collection's slug as its heading, renders each article as a story card, and includes full SEO meta tags (Open Graph and Twitter Card) describing the collection. A back link allows the user to return to their full series list.

## Scenarios

### Viewing a collection with published articles

1. A user navigates to a collection's show path (e.g., `/username/series/:id`).
2. The system loads the collection and its owner.
3. All published articles from the current subforem are retrieved, sorted in ascending chronological order by publication date.
4. Each article is displayed as a story card, with bookmark buttons and local date formatting applied via JavaScript.
5. The page heading shows the collection's slug, and a back link to the user's series index is rendered.

### Viewing an empty collection

1. A user navigates to the show path of a collection that has no published articles.
2. The system loads the collection and finds no articles matching the filter criteria.
3. An empty-state message is displayed in place of the article list.

### SEO meta tags are rendered for the collection page

1. The page head includes a title and description derived from the collection's slug and the community name.
2. Open Graph tags (`og:type`, `og:url`, `og:title`, `og:image`, `og:description`, `og:site_name`) are rendered using the collection's path and the site's main social image.
3. Twitter Card tags (`twitter:card`, `twitter:site`, `twitter:title`, `twitter:description`, `twitter:image:src`) are also rendered.

### Navigating back to the user's series list

1. From the collection show page, the user clicks the back link.
2. The system routes the user to the series index for the collection's owner, listing all of that user's non-empty collections.
