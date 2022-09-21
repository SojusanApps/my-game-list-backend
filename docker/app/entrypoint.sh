#!/bin/sh

case "$1" in
    gunicorn)
        if wait-for-postgresql.py
        then
            gunicorn -c gunicorn.conf.py my_game_list.my_game_list.wsgi:application
        else
            echo "CAN'T CONNECT TO DATABASE!"
        fi
    ;;
    set_state)
        if wait-for-postgresql.py
        then
            my-game-list-manage.py collectstatic --no-input && \
            my-game-list-manage.py migrate --no-input
        else
            echo "CAN'T CONNECT TO DATABASE!"
        fi
    ;;
    *)
        bash -c "$@"
    ;;
esac
