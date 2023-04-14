# CHANGELOG

## v. 1.0.2

* Added configuration for `pre-commit`.
* Added custom pre-push hook for checking if application version and changelog are updated.
* Updated dependencies in requirements.
* Added information in the `README.md` file about installing the `pre-commit` hooks and how to skip the hooks run if needed.
* Added `pre-commit` badge to `README.md` file.

## v. 1.0.1

* Added missing `gettext_lazy` marks.

## v. 1.0.0

* Changed the line length in the project to `120`.
* Added endpoints for the friendship and friendship requests management.
* Changed the name of the field in models from `creation_time` to `created_at` and also `last_modified` to `last_modified_at`.
* Changed the endpoints names to better distinguish between module and endpoints names.
* Added `GameCreateSerializer`.
* Added `ConflictException`.
* Renamed `CreateUserSerializer` to `UserCreateSerializer` and `ListUserSerializer` to `UserSerializer`.

## v. 0.1.0

* Initialization of the project with basic configuration.
