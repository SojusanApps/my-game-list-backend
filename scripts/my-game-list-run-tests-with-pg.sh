#!/bin/sh

export MYGAMELIST_TEST_DB_ENGINE="${MYGAMELIST_TEST_DB_ENGINE:-django.db.backends.postgresql}"
export MYGAMELIST_TEST_DB_NAME="${MYGAMELIST_TEST_DB_NAME:-pytest_postgresql}"
export MYGAMELIST_TEST_DB_USER="${MYGAMELIST_TEST_DB_USER:-pytest_postgresql}"
export MYGAMELIST_TEST_DB_PASSWORD="${MYGAMELIST_TEST_DB_PASSWORD:-pytest_postgresql}"
export MYGAMELIST_TEST_DB_PORT="${MYGAMELIST_TEST_DB_PORT:-55432}"
BASE_DIR="$(realpath $(dirname $0))"
"$BASE_DIR"/my-game-list-run-tests.sh \
    "$@"
