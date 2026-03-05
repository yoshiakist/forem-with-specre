---
id: "01KJ71GQ5Q0CAKGDZFZFFPKXZW"
name: "system_selects_personalized_articles_for_digest"
status: "stable"
last_verified: "2026-02-24"
---

## Related Files

- `app/services/email_digest_article_collector.rb`
- `spec/services/email_digest_article_collector_spec.rb` (Test)

## Functional Overview

`EmailDigestArticleCollector#articles_to_send` selects up to 7 published, digest-eligible articles to include in a user's email digest. Selection is personalized: users who follow tags receive articles from those followed articles filtered by their active subforems; users without tag follows receive featured or tag-matched articles filtered similarly. A composite ranking score rewards high engagement and penalizes clickbait. If the initial query returns fewer than 3 articles, the system broadens its subforem scope to a fallback set. The final list is rotated if the leading article's title was already used as the subject of the most recent digest email. If fewer than 3 articles remain after all stages, an empty array is returned to signal that a digest should not be sent.

## Design Intent

The two-path design (followed-tags vs. no-followed-tags) reflects an intentional quality trade-off: users who actively follow tags get a lower score threshold (> 8) drawing from their personalized feed, while users with no explicit follows get a higher threshold (> 11) applied to featured or broadly-tagged content so they receive only clearly high-quality material. The fallback stage prevents digest suppression for users in small or sparse subforems by expanding the candidate pool to the default subforem rather than silently delivering nothing. Rotating the first article when its title was already a recent subject line avoids recipient fatigue from repetitive subject lines.

## Key Members

- `RESULTS_COUNT: 7` — maximum number of articles to include; determined by a concluded A/B field test (`digest_count_03_18`)
- `CLICK_LOOKBACK: 30` — constant defined on the class (reserved for future click-based filtering)
- `@subforem_ids` — set by `set_subforem_context`; controls which subforem(s) articles are drawn from
- `@skip_subforem_filtering` — when `true`, subforem filter is omitted entirely (applies to users with custom onboarding subforems who have no followed subforems)

## Scenarios

### User with no followed tags receives high-quality articles from their subforem

1. User has no followed tags. The system calls `set_subforem_context` to determine the relevant subforem scope.
2. The system resolves the user's recently-viewed tag names as a fallback interest signal.
3. Articles are fetched that are published after the cutoff date, marked digest-eligible, not authored by the user, have a score above 11, and are either featured or tagged with any of the resolved tags.
4. Results are ordered by the composite ranking formula and limited to 7.
5. If at least 3 articles are found, the list is returned (subject to the rotation check). If fewer than 3, an empty array is returned.

### User with followed tags receives personalized articles from their followed feed

1. User has followed tags. The system calls `set_subforem_context` to determine the subforem scope.
2. Articles are fetched from the user's followed-articles feed that are published after the cutoff date, digest-eligible, not authored by the user, and have a score above 8.
3. Unless subforem filtering is skipped, results are restricted to the user's active subforem IDs.
4. Results are ordered by the composite ranking formula and limited to 7.
5. If at least 3 articles are found, the list is returned (subject to the rotation check). If fewer than 3, the fallback path runs.

### Subforem context is resolved based on user activity and onboarding

1. The system checks the user's all-time subforem activity for any followed subforem IDs.
2. If the user has followed subforems, those IDs are used and subforem filtering is applied normally.
3. If the user has no followed subforems but was onboarded through a non-default custom subforem, subforem filtering is skipped entirely so articles from all subforems are eligible.
4. Otherwise the default subforem ID is used as the sole filter target.

### Fallback broadens scope when fewer than 3 articles are found

1. After the primary query, if fewer than 3 articles are returned, the system enters the fallback stage.
2. If subforem filtering was already being skipped, a site-wide query (score > 11, no subforem filter) is executed.
3. Otherwise, the default subforem ID is appended to the user's subforem list if it is not already present, and the broadened set is queried.
4. Anti-followed tag exclusion is applied to the fallback results if the user has any anti-followed tags.
5. The result is again limited to 7 and ordered by the composite ranking formula. If still fewer than 3, an empty array is returned.

### Article rotation avoids repeating the most recent digest subject line

1. After the article list is assembled, the system checks whether the most recent digest email sent to the user had a subject containing the title of the first article.
2. If it does, the list is rotated by one position so the second article moves to the front.
3. The rotated list is returned, provided it still meets the 3-article minimum.

## Failures / Exceptions

- If the assembled list contains fewer than 3 articles at any stage, `articles_to_send` returns an empty array, signaling to the caller that a digest should not be sent.
- The `cutoff_date` is calculated as 7 days ago, but is floored at 18 hours before the last sent digest to avoid resending very recently seen content; whichever bound is more recent wins.
