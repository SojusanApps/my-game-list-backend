#!/usr/bin/env python
import os
from time import sleep

import psycopg2


def check_database_connection() -> bool:
    """
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
        return True
    except psycopg2.OperationalError:
        return False


def wait_for_database_connection() -> None:
    """
    Wait for PostgreSQL database connection to be established. The timeout is specified in
    the environment variable POSTGRES_CONNECTION_TIMEOUT.
    """
    timeout = float(os.environ.get("POSTGRES_CONNECTION_TIMEOUT", 10))

    i = 0
    interval = 1
    while i < timeout:
        print(f"Waiting for database connection {i}/{timeout} seconds ...")
        if check_database_connection():
            print("SUCCESS: Successfully connected to the PostgreSQL database.")
            return
        i += interval
        sleep(interval)
    else:
        print("FAILED: Connection to PostgreSQL database time out.")


if __name__ == "__main__":
    wait_for_database_connection()
