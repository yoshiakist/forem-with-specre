---
id: "01KJ7041AQY6KB6QP05YZDP44N"
name: "admin_views_experiment_results"
status: "draft"
---

## Related Files

- `app/controllers/field_test/experiments_controller.rb`
- `app/views/field_test/experiments/index.html.erb` (Template)
- `app/views/field_test/experiments/show.html.erb` (Template)
- `app/views/field_test/experiments/_experiments.html.erb` (Template)
- `app/views/field_test/experiments/goal.html.erb` (Template)

## Functional Overview

Experiments are defined in `config/field_test.yml` and activated by deploying the configuration — there is no admin UI for creating, starting, or stopping experiments. `FieldTest::ExperimentsController` provides admins with read-only views for experiment results. The `index` action lists all experiments sorted by start date descending, displaying name, status, dates, and variants (with a winner checkmark). The `show` action renders a single experiment's goals as links plus, for `feed_strategy` experiments, collapsible per-variant configuration details including description, weight, order lever, randomizer flag, relevancy lever parameters, and a fallback/range factor table. The `goal` action narrows the view to one goal within an experiment, showing a results table of participants, conversions, conversion rate, and probability of winning per variant. Invalid experiment IDs or goal names raise `ActionController::RoutingError`.

## Scenarios

### Admin views the experiments index

1. Admin navigates to the experiments index page.
2. The system fetches all experiments and sorts them with the most recently started first.
3. A table is rendered showing each experiment's name (as a link to its detail page), active/completed status, start date, end date, and a list of variants — with a checkmark next to the winning variant if one exists.

### Admin views a specific experiment's detail

1. Admin clicks an experiment name link from the index page.
2. The system looks up the experiment by ID.
3. A detail page is rendered showing the experiment name, a "Back to Experiments" link, and a collapsible "Experiment Details" section (expanded if active) containing links to each goal.
4. If the experiment ID begins with `feed_strategy`, each variant is also shown in its own collapsible section with configuration details: description, weight, order lever, reseed randomizer setting, any relevancy lever query parameters, and a table of fallback and range factors across all levers.

### Admin views results for a specific goal

1. Admin navigates to a goal-specific URL for an experiment.
2. The system looks up the experiment by ID and verifies the requested goal name is registered for that experiment.
3. A focused results table is rendered showing, for each variant: participants, conversions, conversion rate (as a percentage), and probability of winning (shown as "&lt; 1%" when below one percent).
4. The winning variant, if determined, is marked with a checkmark.

### Shared experiments partial renders inline results

1. A page renders the `_experiments` partial, passing a collection of experiments.
2. The partial iterates the experiments in reverse order and, for each, renders the full results table for every goal inline (no link navigation required).
3. For `feed_strategy` experiments, per-variant configuration collapsibles are also rendered within the partial.
4. A "Data Details" link pointing to the experiment's detail page is shown at the bottom of each entry.

## Failures / Exceptions

- If the requested experiment ID is not found (`FieldTest::ExperimentNotFound`), the controller raises `ActionController::RoutingError` with the message "Experiment not found" — resulting in a 404 response.
- If the experiment is found but the requested goal name is not included in the experiment's registered goals, the controller raises `ActionController::RoutingError` with the message "Experiment's goal not found".
