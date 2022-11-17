#!/bin/bash

GREEN="\033[0;32m"
RED="\033[0;31m"
CYAN="\033[0;36m"
RESET="\033[0m"

echo_success()
{
    echo -e "$GREEN $* $RESET"
}

echo_error()
{
    echo -e "$RED $* $RESET"
}

echo_info()
{
    echo -e "$CYAN $* $RESET"
}
