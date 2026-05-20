# MyGameList

A backend service for tracking, rating, and reviewing video games. Users maintain personal game lists, follow games for release notifications, and interact socially through friendships.

## Language

**Dictionary Model**:
A named reference/lookup entity whose primary value is its human-readable name, populated from IGDB or manually. Includes `Genre`, `Platform`, `GameMedia`, `GameMode`, `PlayerPerspective`, `ExternalGameSource`, `Company`, `GameEngine`, `GameType`, and `GameStatus`.
_Avoid_: lookup table, reference data, master data

## Relationships

- A **Dictionary Model** has a canonical English name; Polish translations are optional and fall back to English when absent.
- A **Game** has a language-neutral `slug` always derived from its English `title`.

## Flagged ambiguities

- "dictionary model" applies to `GameType` and `GameStatus` even though their primary fields are named `type` and `status` rather than `name`.
