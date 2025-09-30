#!/usr/bin/env python
"""The task of this module is to provide the functionality to check if the PostgreSQL database is ready to work."""
import os
from time import sleep

import psycopg2
from python_colors import print_error, print_info, print_success


def check_database_connection() -> bool:
    """Check if database accepts a new connection.

    Ping to PostgreSQL database. Database connection parameters should be declared in environment
    variables:
        * POSTGRES_DB - the name of the database,
        * POSTGRES_USER - the name of the database user,
        * POSTGRES_PASSWORD - the password of the database user,
        * POSTGRES_HOST - the hostname of the database,
        * POSTGRES_PORT - the port of the database.

    Returns:
        bool: True if connection ended successfully, False otherwise.
    """
    try:
        connection = psycopg2.connect(
            dbname=os.environ.get("POSTGRES_DB"),
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            host=os.environ.get("POSTGRES_HOST"),
            port=os.environ.get("POSTGRES_PORT"),
        )
        connection.close()
    except psycopg2.OperationalError:
        return False
    else:
        return True


def wait_for_database_connection() -> None:
    """Wait until database connection is established.

    Wait for PostgreSQL database connection to be established. The timeout is specified in
    the environment variable POSTGRES_CONNECTION_TIMEOUT.
    """
    timeout = float(os.environ.get("POSTGRES_CONNECTION_TIMEOUT", "10"))

    i = 0
    interval = 1
    while i < timeout:
        print_info(f"Waiting for database connection {i}/{timeout} seconds ...")
        if check_database_connection():
            print_success("SUCCESS: Successfully connected to the PostgreSQL database.")
            return
        i += interval
        sleep(interval)
    print_error("FAILED: Connection to PostgreSQL database time out.")


def main() -> None:
    """Main entry point."""
    wait_for_database_connection()


if __name__ == "__main__":
    main()
