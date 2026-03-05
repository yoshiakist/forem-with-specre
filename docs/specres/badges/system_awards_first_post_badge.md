---
id: "01KJ6FJVGJTRP7GFQ8571CMTM8"
name: "system_awards_first_post_badge"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/badges/award_first_post.rb`
- `spec/services/badges/award_first_post_spec.rb` (Test)

## Functional Overview

The system awards the "Writing Debut" badge to authors whose first published article falls within a specific time window: published more than one hour ago but no more than one week ago. The award process is gated by several conditions — the article must have a non-negative score, the author must not be flagged as spam or suspended, and the article must be the author's first published piece. When all conditions are met, a `BadgeAchievement` record is created linking the badge to the user.

## Key Members

- `BADGE_SLUG: "writing-debut"` — identifies the specific badge awarded by this service

## Scenarios

### Badge is awarded for a qualifying first article

1. The system looks up the "writing-debut" badge by its slug.
2. The system finds published articles where the publication date is between one hour ago and one week ago.
3. The article has a non-negative score and is the author's first published article.
4. The author has neither a spam nor a suspended role.
5. The system creates a `BadgeAchievement` record associating the badge with the article's author.

### Badge is not awarded when the badge does not exist

1. The system looks up the "writing-debut" badge by its slug.
2. The badge is not found, so the service exits immediately without querying articles.

### Badge is not awarded for articles outside the time window

1. The system finds articles published more than one week ago or less than one hour ago.
2. These articles fall outside the eligible time window and are excluded from the query results.
3. No `BadgeAchievement` record is created.

### Badge is not awarded when the article score is negative

1. The system finds a first article published within the time window.
2. The article's score is below zero.
3. The article is excluded from consideration and no badge is awarded.

### Badge is not awarded to spam or suspended users

1. The system finds a first article published within the time window with a non-negative score.
2. The article's author has either a spam or suspended role.
3. The author is excluded from consideration and no badge is awarded.
