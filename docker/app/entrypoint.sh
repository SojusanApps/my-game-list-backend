#!/bin/sh

case "$1" in
    gunicorn)
        gunicorn -c gunicorn.conf.py my_game_list.my_game_list.wsgi:application
    ;;
    set_state)
        my-game-list-manage.py collectstatic --no-input && \
        my-game-list-manage.py migrate --no-input
    ;;
    *)
        bash -c "$@"
    ;;
esac
