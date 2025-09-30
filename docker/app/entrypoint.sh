#!/bin/sh

case "$1" in
    gunicorn)
        uv run gunicorn -c gunicorn.conf.py my_game_list.my_game_list.wsgi:application
    ;;
    set_state)
        uv run django-admin collectstatic --no-input && \
        uv run django-admin migrate --no-input
    ;;
    *)
        bash -c "$@"
    ;;
esac
