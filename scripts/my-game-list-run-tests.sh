#!/bin/sh

# Get the directory where this script lives, needed for running other scripts.
BASE_DIR="$(realpath "$(dirname "$0")")"

# Load functions for printing with colors
. "$BASE_DIR"/colors.sh

yes_if_defined() {
    [ "$1" ] && printf "yes" || printf "no"
}

no_if_defined() {
    [ "$1" ] && printf "no" || printf "yes"
}
# set RabbitMQ crash log to tmp folder.
export ERL_CRASH_DUMP="${ERL_CRASH_DUMP:-/tmp}"

start_time="$(date +%s)"

extra_pytest_args=""
[ -z "$CI" ] && extra_pytest_args="$extra_pytest_args -vv"
[ -z "$NO_COVERAGE" ] && extra_pytest_args="$extra_pytest_args --cov=my_game_list --cov-report=xml --cov-report=term"

[ -z "$DJANGO_DB_ENGINE" ] && \
    DJANGO_DB_ENGINE="django.db.backends.sqlite3" && \
    POSTGRES_DB: "db.sqlite3"

echo_info "Running pytest."
echo_info "Checking code coverage: $(no_if_defined "$NO_COVERAGE")."
echo_info "Running within CI: $(yes_if_defined "$CI")."
[ "$DJANGO_SETTINGS_MODULE" ] && \
    echo "Using settings from $DJANGO_SETTINGS_MODULE." || \
    echo "The settings module is not overridden by the environment."

echo_info "Extra pytest args: $extra_pytest_args."
# Eval is required here so that extra_pytest_args is properly expanded into arguments.
eval pytest "$extra_pytest_args" --color=yes -n auto tests "$@"
out=$?
echo_success "Pytest execution time: $(($(date +%s) - start_time))s."
exit $out
