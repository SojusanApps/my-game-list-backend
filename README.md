# MyGameList

[![MyGameList CI](https://github.com/SojusanApps/my-game-list-backend/actions/workflows/my-game-list.yml/badge.svg)](https://github.com/SojusanApps/my-game-list-backend/actions/workflows/my-game-list.yml)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=MyGameListPlaceholder_my-game-list-backend&metric=coverage)](https://sonarcloud.io/summary/new_code?id=MyGameListPlaceholder_my-game-list-backend)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![Black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-white.svg)](https://sonarcloud.io/summary/new_code?id=MyGameListPlaceholder_my-game-list-backend)

Application to manage game lists.

## Basic assumptions

* [Python](https://www.python.org/) >= 3.12
* [Django](https://www.djangoproject.com/) >= 4.0
* REST API based on the [Django REST Framework](https://www.django-rest-framework.org/)
* Line length 100
* Language: English
* Tests performed with [pytest](https://docs.pytest.org/)
* Full compatibility with [PEP8](https://peps.python.org/pep-0008/)
* Assumed coverage in tests > 90%
* Automatic tests for PostgreSQL in GitHub CI

## Assumptions about the release preparation and deployment methodology

1. I keep 2 branches:
   * **master**: The master branch of the repository contains the fully functional production code.
   * **devel**: The branch for development contains the functional code with new features.
1. I use versioning following the [semver 2.0](https://semver.org/spec/v2.0.0.html)
1. The `master` and `devel` branches should contain stable and working code.
1. Workflow:
    * The developer is preparing a branch with new functionality or a correction, giving it a name as *[bugfix/feature/hotfix]/[description]*, e.g. *feature/new-document*
    * When the code is ready, the developer prepares PR (Pull Request) for the **devel** branch for new functionalities
    * If all functionalities work, the code is uploaded to the **master** branch

Tag Legend:

* **latest** - The latest production version.

## Deploy

1. Create the file `docker-compose.yaml` and upload it to the production server. (only the first time)
1. Log in via ssh to the production server and execute the following commands:

   ```shell
   docker compose -f docker-compose.yml pull
   docker compose -f docker-compose.yml up --detach --force-recreate --remove-orphans
   ```

## Local installation

1. Clone the repository from GitHub with the command:

   ```shell
   https://github.com/SojusanApps/my-game-list-backend.git
   ```

1. Create a virtual environment with [virtualenvwrapper](https://github.com/regisf/virtualenvwrapper-powershell):

   ```shell
   MkVirtualEnv my-game-list
   ```

1. Activate the virtual environment:

   ```shell
   WorkOn my-game-list
   ```

1. Update the pip package:

   ```shell
   pip install -U pip
   ```

1. Install all project dependencies:

   ```shell
   pip install -r requirements/requirements-all.txt
   ```

1. Install the project locally:

   ```shell
   pip install -e .
   ```

1. Install the `pre-commit` hooks:

   ```shell
   pre-commit install --hook-type pre-commit --hook-type pre-push
   ```

   To disable checking of certain hooks, you can use the `SKIP` variable, e.g.:

   ```shell
   SKIP=check-version-and-changelog git push
   ```

1. Create a new PostgreSQL database in docker:

   ```shell
   docker run --name my_game_list_postgresql -p 5432:5432 -e POSTGRES_DB=my_game_list -e POSTGRES_USER=my_game_list -e POSTGRES_PASSWORD=my_game_list -d postgres:15.3-alpine
   ```

1. Run database migrations:

   ```shell
   my-game-list-manage.py migrate
   ```

1. Create a Django admin account:

   ```shell
   my-game-list-manage.py createsuperuser
   ```

1. Start the development server:

   ```shell
   my-game-list-manage.py runserver
   ```

The application is available at [http://127.0.0.1:8000](http://127.0.0.1:8000).
Access to the admin panel is available at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin), you can follow it and log in with the data (login and password) provided to the command `my-game-list-manage.py createsuperuser`.

## Configuration

* All configurations can be found in `my_game_list/settings/`
* **base.py** - contains the base configuration of the application
* **devel.py** - includes development configuration
* **test.py** - contains configuration for tests
* You can set up any configuration file using the `DJANGO_SETTINGS_MODULE` environment variable

## Swagger

Swagger enables you to visualize and interact with a RESTful API. It generates automatically based on the OpenAPI specification, a list of available endings along with the documentation contained in the code. In addition, it presents examples of data structures that should be sent to a given end and enables direct interaction with them.

Swagger is available at: [http://127.0.0.1:8000/api/my-game-list/](http://127.0.0.1:8000/api/my-game-list/)

## Tests

1. Running tests using the PostgreSQL database:

   ```shell
   my-game-list-run-tests-with-pg.sh
   ```

2. Starting the full test stack with the tox utility:

   ```shell
   tox
   ```
