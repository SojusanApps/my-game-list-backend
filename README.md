# MyGameList

[![codecov](https://codecov.io/gh/Sojusan/my-game-list/branch/master/graph/badge.svg?token=knlIznGzJO)](https://codecov.io/gh/Sojusan/my-game-list)

Application to manage game lists.

## Basic assumptions

* [Python](https://www.python.org/) >= 3.10
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
    * The developer is preparing a branch with a new functionality or an correction, giving it a name as *[bugfix/feature/hotfix]-[description]*, e.g. *feature-new-document*
    * When the code is ready, the developer prepares MR (Merge Request) for the **devel** branch for new functionalities
    * If all functionalities work, the code is uploaded to the **master** branch

Tag Legend:

* **latest** - The latest production version.

## Deploy

1. Create the file `docker-compose.yaml` and upload it to the production server. (only the first time)
1. Log in via ssh to the production server and execute the following commands:

   ```shell
   docker-compose -f docker-compose.yml pull
   docker-compose -f docker-compose.yml up --detach --force-recreate --remove-orphans
   ```

## Local installation

1. Clone the repository from GitLab with the command:

   ```shell
   https://github.com/Sojusan/my-game-list.git
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

1. Create a new PostgreSQL database in docker:

   ```shell
   docker run --name my_game_list_postgresql -p 5432:5432 -e POSTGRES_DB=my_game_list -e POSTGRES_USER=my_game_list -e POSTGRES_PASSWORD=my_game_list -d postgres:14.4-alpine
   ```

1. Create a database:

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
Access to the admin panel is available at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin), you can follow it log in with the data (login and password) provided to the command `my-game-list-manage.py createsuperuser`.

## Configuration

* All configuration can be found in `my_game_list/settings/`
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
