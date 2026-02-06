# CHANGELOG

> Date format is DD.MM.YYYY.

## v. [4.8.0] - 30.01.2026

* Added Bruno endpoints for collections.
* Added `Collections` app.

## v. [4.7.1] - 21.01.2026

* Fix the m2m relation import in the `import_data_from_igdb.py` script for games objects.

## v. [4.7.0] - 01.01.2026

* Improvements to game queries to make them faster.
* Added additional information to the Game model:
  * `GameEngine`
  * `GameMode`
  * `PlayerPerspective`
  * `GameType`
  * `GameStatus`
* Updated the `Game` list endpoint to include the game status and type.
* Updated the `Game` retrieve endpoint to include the new data.
* Updated the `Game` filters.

## v. [4.6.0] - 28.12.2025

* Changed the `User` model `str` method.
* Removed `all-values` endpoints.
* Added `CompanyGameSerializer` and `CompanyDetailSerializer`.
* Fixed the ordering for the `latest_game_updates` in the user details.

## v. [4.5.0] - 26.12.2025

* Added `notifications` application.
* Added a notification when user send/accepts the friend request.

## v. [4.4.0] - 25.12.2025

* Updated the Python version to 3.14.
* Updated dependencies in requirements.

## v. [4.3.0] - 21.12.2025

* Added `igdb_updated_at` to models:
  * `Game`, `Platform`, `Genre` and `Company`
* Improved the IGDB import script to be based on the `updated_at`, so only the newest updates will be processed.
* Move `dev` dependencies into `[dependency-groups]`.

## v. [4.2.5] - 26.11.2025

* Added [django-tui](https://github.com/anze3db/django-tui) - a package that adds a terminal user interface for django commands.
* Updated dependencies in requirements.

## v. [4.2.4] - 03.09.2025

* Migrate to [uv](https://docs.astral.sh/uv) package manager.
* Added a new settings file for mypy type checker.
* Update Docker files to be compatible with uv package manager.
* Divided the tox commands into separate envs.
* Added [typer](https://github.com/fastapi/typer) for command line interface.
  * Changed `my-game-list-build.py` script to use `typer`.
* Updated the GitHub Action configuration to work with uv.
* Upgraded PostgreSQL version to `18.0`.
* Changed the GitHub Action to use commit SHA instead of tags.

## v. [4.2.3] - 28.08.2025

* Updated dependencies in requirements.
* Adjust code typing to fix mypy issues.
* Updated SonarQube Github action scanner.
* Updated the prometheus metrics endpoint to accept only GET request.

## v. [4.2.2] - 11.02.2025

* Updated dependencies in requirements.
* Added missing migration.

## v. [4.2.1] - 10.02.2025

* Added a new make command (`generate_openapi`) to generate the `openapi.json` file.
* Fixed the openapi schema using the `drf-spectacular`.
* Changed the `ApiVersion` to return a structured output instead of raw string.

## v. [4.2.0] - 14.01.2025

* Added `GameMedia` model in `game` app.
* Added `owned_on` to `GameList` model.1

## v. [4.1.3] - 05.12.2024

* Added base class for IGDB models `IGDBModel`.
* Improvements to IGDB integrations.

## v. [4.1.2] - 02.11.2024

* Changed the way of handling the source code, from individual file for each object to a single one for all.

## v. [4.1.1] - 02.11.2024

* Cleanup in `docker-compose.yml`:
  * Use depends on condition for waiting for database instead of custom script,
  * Fix running the application as non-root user.

## v. [4.1.0] - 11.09.2024

* Removed the `avatar` field from the `User` model.
* For avatars now will be used `Gravatar`.
* Removed the `FileSizeValidator` as it is no longer needed.
* Removed the environment variable `MGL_LIMIT_FILE_SIZE` as it is no longer needed.

## v. [4.0.0] - 10.09.2024

* Integrated with the IGDB database.
* Removed the development example data as the process is changed in favor of the IGDB database.
* Updated dependencies in requirements.
* Removed the `requirements-deploy.txt` file.
* Updated `Bruno` endpoints.
* Fixed `ruff` configuration.
* Added new environment variables to `example.env` (`IGDB_CLIENT_ID` and `IGDB_CLIENT_SECRET`).
* Added new model `Company`.
* Removed old models for `Developer` and `Publisher`, they are now in the new `Company` model.
* Changed the `Genre`, `Game`, `Platform` and `Company` models to be compatible with IGDB data.
* Changed the `game_cover_image` field in the `GameListSerializer` to be `CharField` instead of `FileField`.
* Added `igdb_id` field to the `Game`, `Company`, `Genre` and `Platform` models, as those are now objects integrated with external IGDB database.
* Renamed the `dictionary` field into `summary` in the `Game` model.
* Added `abbreviations` field to the `Platform` model.
* Removed the `django_cleanup` dependency.
* Updated tests to reflect the changes made to models.
* Updated dependencies in the `pre-commit` configuration.

## v. [3.3.0] - 12.06.2024

* Added new development data regarding the developers and publishers.
* Added a new field for the company logo for developers and publishers.

## v. [3.2.0] - 15.05.2024

* Added `Bruno` endpoints for development.
* Added `status_code` to game list endpoints.
* Added `game_id` to the `GameListSerializer`.
* Removed `logged_in_user` action for the `user` endpoint.

## v. [3.1.0] - 13.05.2024

* Fixed `GameListSerializer` to return the cover image url.
* Fixed `UserDetailSerializer` to return the image urls for nested objects.
* Added `logged_in_user` - new action for the `user` endpoint to get the details of the logged in user.

## v. [3.0.1] - 10.05.2024

* Calculation of the rank position is fixed. Right now the average store will have `0` instead of `none` when there is no scores for the game.
* Added `load_development_data` - new make command to load development data.

## v. [3.0.0] - 09.05.2024

* Changed `BinaryField` to `ImageField` for `game_cover` and `avatar`.
* Added `average_score`, `scores_count`, `rank_position`, `members_count`, and `popularity` to `Game` models.
* Added new dependency `django-cleanup` to automatically cleanup media files.
* Added new setting `LIMIT_FILE_SIZE`, to control the size of the uploaded images.
* Added `FileSizeValidator` - validator of the uploaded file size.
* Added development setting for working with media files.
* Added ordering settings for `Game` views.
* Added `GameQuerySet`.

## v. [2.2.0] - 03.04.2024

* Updated few models and serializers:
  * GameReview
  * GameList
  * User
* Moved `score` from `GameReview` to `GameList`.
* Added `GameListCreateSerializer`.
* Added `Gender` to `User` model.

## v. [2.1.3] - 06.03.2024

* Added user details to GameReview endpoint.

## v. [2.1.2] - 21.02.2024

* Updated the Python version to 3.12.
* Enabled coverage reporting in the SonarCloud.
* Removed Codecov from the project.

## v. [2.1.1] - 17.12.2023

* Upgrade project dependencies.

## v. [2.1.0] - 08.09.2023

* Added image preview to admin panels.
* Added filters to all endpoints.
* Added `django-filter-stubs` to project dependencies.
* Added `status_full_name` to return game list status as human readable string.

## v. [2.0.1] - 24.08.2023

* Update project dependencies.
* Add stubs for `py`.

## v. [2.0.0] - 14.07.2023

* Changed the username field from `username` to `email`.

## v. [1.1.4] - 29.06.2023

* Added `mypy`.

## v. [1.1.3] - 26.06.2023

* Activate more ruff rules.
* `.gitattributes` file added.

## v. [1.1.2] - 23.06.2023

* Resolve warnings from SonarLint.
* Upgraded the dependencies.
* Added tests for the application logic.
* Added `if TYPE_CHECKING` code block to be ignored by coverage.
* Added helper functions to Makefile for starting the database for development and testing.
* Configure application docker image to run as a non-root user.
* Fixed error with type hinting in the manager for the `Friendship`.
* Added `pytest-xdist` to run tests in parallel.
* Added `pytest-sugar` to improve the tests output.

## v. [1.1.1] - 05.06.2023

* Added configuration for SonarCloud analysis tool.

## v. [1.1.0] - 19.05.2023

* Corrected the Dockerfiles to be compatible with hadolint validation.
* Added `LABEL` to Dockerfiles to automatically link an image to a GitHub repository.
* Added Grafana configuration.
* Added Loki configuration.
* Added Prometheus configuration.
* Added Promtail configuration.
* Created the logging configuration for the application.
* Added custom prometheus metrics for cpu and memory usage.
* Added new decorators for metrics usage.
* Added new dependencies:
  * docker
  * django_prometheus
  * prometheus-client
  * psutil
* Improved scripts (limitation of running shell commands.)

## v. [1.0.3] - 19.04.2023

* Changed the linter to `ruff`.

## v. [1.0.2] - 14.04.2023

* Added configuration for `pre-commit`.
* Added custom pre-push hook for checking if application version and changelog are updated.
* Updated dependencies in requirements.
* Added information in the `README.md` file about installing the `pre-commit` hooks and how to skip the hooks run if needed.
* Added `pre-commit` badge to `README.md` file.

## v. [1.0.1] - 03.04.2023

* Added missing `gettext_lazy` marks.

## v. [1.0.0] - 02.04.2023

* Changed the line length in the project to `120`.
* Added endpoints for the friendship and friendship requests management.
* Changed the name of the field in models from `creation_time` to `created_at` and also `last_modified` to `last_modified_at`.
* Changed the endpoints names to better distinguish between module and endpoints names.
* Added `GameCreateSerializer`.
* Added `ConflictException`.
* Renamed `CreateUserSerializer` to `UserCreateSerializer` and `ListUserSerializer` to `UserSerializer`.

## v. [0.1.0] - 03.08.2022

* Initialization of the project with basic configuration.
