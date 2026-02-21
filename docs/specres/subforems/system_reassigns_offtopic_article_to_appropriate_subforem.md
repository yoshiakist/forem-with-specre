---
id: "01KHYYF2GKNFJF3ZE6PR6X8X9V"
name: "system_reassigns_offtopic_article_to_appropriate_subforem"
status: "stable"
last_verified: "2026-02-21"
---

## Related Files

- app/services/subforem_reassignment_service.rb
- app/services/ai/subforem_finder.rb
- spec/services/subforem_reassignment_service_spec.rb (Test)

## Functional Overview

When an article receives an off-topic automod label (e.g., `ok_but_offtopic_for_subforem`), the `SubforemReassignmentService` evaluates whether the article should be moved to a more appropriate subforem. It checks that the article is not spam, respects the author's reassignment preference, then uses `Ai::SubforemFinder` to analyze the article content against available subforems via an LLM prompt. If a better match is found, the article's subforem is updated, the automod label is changed to its on-topic equivalent, and a subforem change notification is queued for the author.

## Design Intent

AI-powered reassignment keeps content well-organized across subforems without requiring manual moderator intervention. The service respects user autonomy by honoring the `disallow_subforem_reassignment` user setting, and falls back gracefully when the AI cannot find a match (defaulting to the misc subforem or leaving the article in place).

## Key Members

- `automod_label` — The AI-generated moderation label on the article that triggers reassignment evaluation
- `disallow_subforem_reassignment` — User setting that opts out of automatic reassignment

## Scenarios

### System reassigns an off-topic article

1. An article has an automod label matching an off-topic pattern (e.g., `ok_but_offtopic_for_subforem`, `very_good_but_offtopic`, `great_but_off_topic`)
2. System verifies the article is not flagged as spam or harmful
3. System checks the author's `disallow_subforem_reassignment` setting (defaults to allowing if nil)
4. `Ai::SubforemFinder` builds a prompt with the article content and available subforem descriptions, then queries the LLM
5. If the LLM identifies a better-matching subforem, the article's `subforem_id` is updated
6. The automod label is changed to its on-topic equivalent (e.g., `ok_but_offtopic_for_subforem` becomes `okay_and_on_topic`)
7. System queues a `Notifications::SubforemChangeNotificationWorker` to notify the author

### System skips reassignment for on-topic articles

1. An article has an on-topic automod label (e.g., `okay_and_on_topic`, `very_good_and_on_topic`)
2. System determines no reassignment is needed and returns false

### System skips reassignment for spam articles

1. An article has a spam or harmful label (e.g., `clear_and_obvious_spam`, `likely_spam`, `harmful`)
2. System skips reassignment entirely to avoid promoting bad content

### System respects user opt-out

1. The article author has `disallow_subforem_reassignment` set to true
2. System skips reassignment and returns false

## Failures / Exceptions

- If the AI service raises an error, the service catches it, logs the error, and returns false without reassigning
- If no appropriate subforem is found by the AI, the article remains in its current subforem
