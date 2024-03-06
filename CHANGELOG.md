# CHANGELOG

> Date format is DD.MM.YYYY.

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

* Corrected the Dockerfiles to meet hadolint validation.
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
