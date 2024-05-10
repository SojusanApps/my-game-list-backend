# The @ makes sure that the command itself isn't echoed in the terminal
help:
	@echo "MyGameList Makefile"
	@echo "run - Start the application on the default port."
	@echo "fresh_run - Use for the first start of the application. It collects the static files,"
	@echo "            runs the migrations, prompts for superuser creation, and at the end runs the application."
	@echo "check - Check the correctness of code with black formatter and ruff."
	@echo "translations - Prepare the translations for supported languages."
	@echo "coverage - Prepare the coverage report in HTML format."
	@echo "test_db - Run a Docker container with test database."
	@echo "app_db - Run a Docker container with app database."
	@echo "test - Run all tests for the application."
	@echo "load_development_data - Load development data into the local database."

run:
	my-game-list-manage.py runserver

translations:
	my-game-list-manage.py makemessages -l pl

fresh_run:
	my-game-list-manage.py collectstatic
	my-game-list-manage.py makemigrations
	my-game-list-manage.py migrate
	my-game-list-manage.py createsuperuser
	my-game-list-manage.py runserver

check:
	black .
	ruff check .
	mypy . --strict

coverage:
	coverage html

app_db:
	docker run --name my_game_list_postgresql -p 5432:5432 -e POSTGRES_DB=my_game_list -e POSTGRES_USER=my_game_list -e POSTGRES_PASSWORD=my_game_list -d postgres:15.3-alpine

test_db:
	docker run --name pytest_postgresql -e POSTGRES_USER=pytest_postgresql -e POSTGRES_PASSWORD=pytest_postgresql -e POSTGRES_DB=pytest_postgresql -p 127.0.0.1:9999:5432 -d postgres:15.3-alpine

test:
	pytest -n auto

load_development_data:
	cp -r development/cover_images media/
	my-game-list-manage.py loaddata development/development-data.json

# .PHONY defines parts of the makefile that are not dependant on any specific file
# This is most often used to store functions
.PHONY: help run fresh_run check translations app_db test_db coverage
