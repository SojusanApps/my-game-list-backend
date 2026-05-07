# PRD: Business-Level Prometheus Metrics

Status: needs-triage

---

## Problem Statement

The application already exposes infrastructure-level Prometheus metrics (CPU usage, memory usage) and Django request/response metrics via `django_prometheus`. However, there are no domain-level metrics that answer business questions — for example, "Is the application actively gaining new users?" or "Are users engaging with the game-list feature?". Without these counters, Grafana dashboards cannot show growth trends or engagement signals.

## Solution

Add two new Prometheus `Counter` metrics to the application:

1. **`users_registered_total`** — increments every time a new user account is created, regardless of the creation path (API, admin panel, management commands).
2. **`game_lists_entries_created_total`** — increments every time a user adds a game to their game list.

Both counters are wired via Django `post_save` signals so they capture all creation paths, not just the REST API. In Grafana, a PromQL expression like `increase(users_registered_total[1d])` immediately produces a "new users per day" time series suitable for a dashboard panel.

## User Stories

1. As an operator, I want to see how many new users registered per day, so that I can monitor whether the application is growing.
2. As an operator, I want to see the total number of registered users over time, so that I can report on cumulative growth.
3. As an operator, I want to see how many game-list entries were created per day, so that I can assess whether existing users are actively engaging with the app.
4. As an operator, I want to query both metrics in PromQL, so that I can build Grafana dashboard panels without any additional data sources.
5. As a developer, I want the metrics to be defined in a single, central `Metrics` class, so that all custom metrics remain discoverable in one place.
6. As a developer, I want the counters incremented via Django signals, so that they capture every creation path (API, admin, management commands) without duplicating instrumentation logic.
7. As a developer, I want the user-registration signal wired through `UsersConfig.ready()`, consistent with how game signals are already wired in `GamesConfig.ready()`.

## Implementation Decisions

- **Metric type:** `Counter` (from `prometheus_client`) for both metrics. Counters are monotonically increasing and map directly to Grafana's `increase()` / `rate()` functions for "per day" dashboards. The existing metrics (`cpu_usage_metric`, `memory_usage_metric`) are `Gauge`; the new metrics are a distinct type and should not be confused with them.
- **Central registry:** Both counters are added as class attributes on the existing `Metrics` class in the core metrics module — consistent with current `cpu_usage_metric` and `memory_usage_metric`.
- **Signal hook — users:** A new `users/signals.py` module is created with a `post_save` receiver on the `User` model that calls `counter.inc()` when `created=True`. The `UsersConfig.ready()` method in `users/apps.py` imports this module (matching the pattern already used in `GamesConfig.ready()`).
- **Signal hook — game lists:** A new `post_save` receiver on `GameList` is added to the existing `games/signals.py`, guarded by `created=True`, that increments `game_lists_entries_created_total`.
- **No labels:** Both counters are flat (no Prometheus label dimensions). This keeps the implementation simple and avoids high-cardinality concerns.
- **No schema changes:** These are in-memory Prometheus metrics; no database migrations are required.

## Testing Decisions

A good test for these metrics verifies **external observable behavior**: after performing the action (user created, game-list entry created), the counter value has increased by exactly 1. Tests should not inspect signal internals or the `Metrics` class attributes directly — they should simulate the real creation path and assert the counter state.

**Modules to test:**

- `users/signals.py` — assert `users_registered_total` increments by 1 when a `User` is saved with `created=True`, and does not increment on update.
- `games/signals.py` (the new receiver) — assert `game_lists_entries_created_total` increments by 1 when a `GameList` is saved with `created=True`, and does not increment on update or delete.

**Prior art:** The existing `games/signals.py` tests (if any) and `django_prometheus.testutils` helpers (`save_registry`, `assert_metric_diff`) are the natural model for these tests. The pattern of using `post_save` with `created=True` guard already appears in `games/signals.py` (`create_game_stats`).

## Out of Scope

- Login / session metrics (`user_logins_total`) — JWT authentication does not emit a Django signal; hooking this would require additional middleware or a custom token view, which is a separate concern.
- Labelled breakdown of `game_lists_entries_created_total` by `GameListStatus` — explicitly decided against during design to keep the metric flat.
- Grafana dashboard definitions — dashboard JSON/provisioning files are out of scope; the counters are the deliverable, dashboards are the operator's responsibility.
- Metrics for games added to the catalogue (`games_added_total`), friendships, or notifications — deferred for a future iteration.

## Further Notes

- Both counters survive application restarts at zero; Grafana's `increase()` function handles counter resets correctly via the `reset detection` built into PromQL.
- The Prometheus scrape endpoint is already exposed at `/prometheus/metrics` via `custom_export_to_django_view` and is scraped by the existing Prometheus instance in `docker/prometheus/prometheus.yml`.
