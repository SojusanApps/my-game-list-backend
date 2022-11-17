#!/usr/bin/env python
GREEN = "\033[0;32m"
RED = "\033[0;31m"
YELLOW = "\033[0;33m"
CYAN = "\033[0;36m"
RESET = "\033[0m"


def print_color(color: str, text: str):
    print(f"{color} {text} {RESET}")


def print_success(text: str):
    print_color(GREEN, text)


def print_error(text: str):
    print_color(RED, text)


def print_info(text: str):
    print_color(CYAN, text)


def print_warning(text: str):
    print_color(YELLOW, text)
