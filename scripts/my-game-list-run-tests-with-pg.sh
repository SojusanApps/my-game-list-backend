#!/bin/sh -e

# Get the directory where this script lives, needed for running other scripts.
BASE_DIR="$(realpath "$(dirname "$0")")"

# Load functions for printing with colors
. "$BASE_DIR"/colors.sh

DJANGO_DB_ENGINE="${DJANGO_DB_ENGINE:-django.db.backends.postgresql}"
POSTGRES_DB="${POSTGRES_DB:-pytest_postgresql}"
POSTGRES_USER="${POSTGRES_USER:-pytest_postgresql}"
POSTGRES_PASSWORD="${POSTGRES_PASSWORD:-pytest_postgresql}"
POSTGRES_HOST="${POSTGRES_HOST:-127.0.0.1}"
POSTGRES_INTERNAL_PORT="${POSTGRES_INTERNAL_PORT:-5432}"
POSTGRES_NAME="${POSTGRES_NAME:-pytest_postgresql}"

POSTGRES_IMAGE="${POSTGRES_IMAGE:-postgres:18.0-alpine}"
POSTGRES_EXTERNAL_PORT="${POSTGRES_EXTERNAL_PORT:-9999}"
POSTGRES_PORT_MAP="127.0.0.1:$POSTGRES_EXTERNAL_PORT:$POSTGRES_INTERNAL_PORT"
POSTGRES_PORT="$POSTGRES_EXTERNAL_PORT"

echo_info "Configuration:"
echo_info "DJANGO_DB_ENGINE: $DJANGO_DB_ENGINE"
echo_info "POSTGRES_DB: $POSTGRES_DB"
echo_info "POSTGRES_USER: $POSTGRES_USER"
echo_info "POSTGRES_PASSWORD: $POSTGRES_PASSWORD"
echo_info "POSTGRES_HOST: $POSTGRES_HOST"
echo_info "POSTGRES_INTERNAL_PORT: $POSTGRES_INTERNAL_PORT"
echo_info "POSTGRES_EXTERNAL_PORT: $POSTGRES_EXTERNAL_PORT"
echo_info "POSTGRES_NAME: $POSTGRES_NAME"
echo_info "POSTGRES_IMAGE: $POSTGRES_IMAGE"
echo_info "POSTGRES_PORT: $POSTGRES_PORT"
echo_info "POSTGRES_PORT_MAP: $POSTGRES_PORT_MAP"

# Add a hook, which tries to kill the container running at the exit and in case of SIGINT.
# First arg set to anything means handling SIGINT.
end() {
    out=$?
    trap - EXIT
    echo_info "Running exit handler."
    if [ "$1" ]
    then
        echo_info "Caught SIGINT/Ctrl+C."
        out=1
    fi
    [ $out -ne 0 ] && echo "Tests failed."
    [ "$POSTGRESQL_CONTAINER_STARTED" ] && \
        echo_info "Trying to stop and remove the PostgreSQL container." && \
        (docker rm -f "$POSTGRES_NAME" > /dev/null || true)
    exit $out
}
trap end EXIT
trap "end 1" INT
# Only try to run the container if not ran by CI, as
# CI already provides a PostgreSQL container for us.
if [ -z "$CI" ]
then
    set +e
    out=$(docker ps -a -q -f name="$POSTGRES_NAME" 2>&1)
    code=$?
    set -e
    [ $code != 0 ] && \
        echo_error "Can't check if the container is running. Maybe docker is not working? Docker ps output:" && \
        echo_error "$out" && \
        exit 1
    if [ -z "$out" ]
    then
        echo_info "PostgreSQL is not running. Trying to start it in a docker container."
        set +e
        out=$(docker run \
            --name "$POSTGRES_NAME" \
            -e "POSTGRES_USER=$POSTGRES_USER" \
            -e "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" \
            -e "POSTGRES_DB=$POSTGRES_DB" \
            -p "$POSTGRES_PORT_MAP" \
            -d "$POSTGRES_IMAGE" \
            2>&1
        )
        code=$?
        set -e
        if [ $code = 0 ]
        then
            POSTGRESQL_CONTAINER_STARTED=1
            echo_info "Container started."
        else
            echo_error "Can't start the container. Docker run output:"
            echo_error "$out"
            exit 1
        fi
    else
        echo_error "Can't start the container for PostgreSQL, because a container with the name"
        echo_error "$POSTGRES_NAME already exists. If you're sure you don't need it,"
        echo_error "you can remove it with: docker rm -f $POSTGRES_NAME"
        exit 1
    fi
else
    echo_info "Running within CI."
    echo_info "If that's not true, please remove the 'CI' variable from the environment"
    echo_info "e.g. by running 'unset CI' and re-run."
fi

# Set explicitly this env var because otherwise it'll be overridden in my-game-list-run-tests.sh.
export DJANGO_DB_ENGINE POSTGRES_USER POSTGRES_PASSWORD POSTGRES_DB POSTGRES_NAME POSTGRES_HOST POSTGRES_PORT

echo_info "Waiting for the PostgreSQL to be available."
"$BASE_DIR"/wait-for-postgresql.py
echo_info "Running tests against PostgreSQL."
"$BASE_DIR"/my-game-list-run-tests.sh \
    "$@"
