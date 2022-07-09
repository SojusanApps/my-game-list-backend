#!/bin/sh

yes_if_defined() {
    [ "$1" ] && printf "yes" || printf "no"
}

no_if_defined() {
    [ "$1" ] && printf "no" || printf "yes"
}
# set RabbitMQ crash log to tmp folder.
export ERL_CRASH_DUMP="${ERL_CRASH_DUMP:-/tmp}"

start_time="$(date +%s)"
# Get directory where this script lives, needed for running other scripts.
BASE_DIR="$(realpath $(dirname $0))"

extra_pytest_args=""
[ -z "$CI" ] && extra_pytest_args="$extra_pytest_args -vv"
[ -z "$NO_COVERAGE" ] && extra_pytest_args="$extra_pytest_args --cov=my_game_list"
[ -z "$POSTGRES_TESTS" ] && extra_pytest_args="$extra_pytest_args -m \"not postgresql\""

echo "Running pytest."
echo "Checking code coverage: $(no_if_defined $NO_COVERAGE)."
echo "Running witihn CI: $(yes_if_defined $CI)."
[ "$DJANGO_SETTINGS_MODULE" ] && \
    echo "Using settings from $DJANGO_SETTINGS_MODULE." || \
    echo "Settings module not overriden by environment."
# Eval is required here so that extra_pytest_args is properly
# expanded into arguments.
eval pytest $extra_pytest_args --color=yes tests "$@"
out=$?
echo "Pytest execution time: $(($(date +%s) - $start_time))s."
exit $out
