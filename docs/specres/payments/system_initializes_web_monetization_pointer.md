---
id: "01KJVDWABE6Y2TMWKY0JGNVWGF"
name: "system_initializes_web_monetization_pointer"
status: "draft"
---

## Related Files

- `app/assets/javascripts/initializers/initializePaymentPointers.js`

## Functional Overview

When an article page loads, the system sets the Web Monetization meta tag's content to the appropriate payment pointer. If the article's author has a payment pointer embedded in the page, that pointer is used preferentially. If no author-specific pointer is present, the system falls back to the site-wide base payment pointer. This ensures the correct monetization recipient is registered with the browser for every page view.

## Design Intent

The two-level fallback (author pointer first, site base pointer second) reflects Forem's support for creator monetization: article authors should receive direct web monetization payments when their own pointer is configured, while the platform's base pointer serves as the default when no author pointer exists. Reading the pointers from DOM data attributes rather than JavaScript variables keeps the configuration server-rendered and avoids an additional client-side fetch.

## Scenarios

### Author has a payment pointer configured

1. The page renders with an element carrying the author's payment pointer in a data attribute.
2. The monetization meta tag is already present in the page head.
3. The initializer reads the author's payment pointer from the DOM element.
4. The initializer sets the monetization meta tag's content to the author's payment pointer.

### Author has no payment pointer; site base pointer is configured

1. The page renders without an author payment pointer element, but includes a site-wide base payment pointer element.
2. The initializer finds no author payment pointer element.
3. The initializer reads the base payment pointer from the site-wide DOM element.
4. The initializer sets the monetization meta tag's content to the base payment pointer.

### Neither author nor base payment pointer is present

1. The page renders without either a author payment pointer element or a base payment pointer element.
2. The initializer finds neither element and takes no action, leaving the monetization meta tag unchanged (or absent).
