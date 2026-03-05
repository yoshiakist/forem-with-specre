---
id: "01KHZ2CEBFEA1C3PMCCZPQ5JQF"
name: "system_exposes_opensearch_descriptor"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- `app/controllers/open_search_controller.rb`
- `app/views/open_search/show.xml.erb` (Template)
- `spec/requests/open_search_spec.rb` (Test)

## Functional Overview

The system serves an OpenSearch Description Document at `/open-search.xml`, enabling browsers and search clients to discover and integrate with the platform's search functionality. When a browser detects this descriptor, it can offer the site as a search provider in its address bar. The XML document contains the community name, a description, contact email, and the search URL template pointing to `/search?q={searchTerms}`.

## Scenarios

### Browser discovers the OpenSearch descriptor

1. A browser or search client requests `/open-search.xml`
2. `OpenSearchController#show` renders the XML template with appropriate cache headers
3. The response includes the community name from `Settings::Community.community_name`
4. The search URL template is set to `/search?q={searchTerms}` for the current site
5. The surrogate key header is set to `"open-search-xml"` for CDN cache management

### Descriptor contains correct site metadata

1. The XML includes a `ShortName` element with the community name
2. The XML includes a `Description` element describing the search capability
3. The XML includes a `Contact` element with the community email
4. The `Url` element specifies the search endpoint with `{searchTerms}` placeholder for query substitution
