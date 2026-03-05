import os
import mysql.connector


def get_connection():
    """
    Central MySQL connection factory.
    Uses environment variables so it works both locally and with Docker.
    """
    host = os.getenv("SWIMS_DB_HOST", "127.0.0.1")
    port = int(os.getenv("SWIMS_DB_PORT", "3306"))
    user = os.getenv("SWIMS_DB_USER", "swims_user")
    password = os.getenv("SWIMS_DB_PASSWORD", "swims_pass")
    database = os.getenv("SWIMS_DB_NAME", "swims")

    return mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )