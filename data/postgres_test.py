"""
Test connection between AI Machine Doctor and PostgreSQL.
"""

import os

import pg8000
from dotenv import load_dotenv


# ============================================================
# Load environment variables
# ============================================================

load_dotenv()


def main():

    host = os.getenv("POSTGRES_HOST", "localhost")
    port = int(os.getenv("POSTGRES_PORT", "5432"))
    database = os.getenv(
        "POSTGRES_DB",
        "ai_machine_doctor",
    )
    user = os.getenv(
        "POSTGRES_USER",
        "postgres",
    )
    password = os.getenv(
        "POSTGRES_PASSWORD",
    )

    print()
    print("=" * 60)
    print("       AI MACHINE DOCTOR - POSTGRESQL TEST")
    print("=" * 60)

    print(f"Host     : {host}")
    print(f"Port     : {port}")
    print(f"Database : {database}")
    print(f"User     : {user}")
    print()

    try:

        # ----------------------------------------------------
        # Connect to PostgreSQL
        # ----------------------------------------------------

        connection = pg8000.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )

        print(
            "[POSTGRES] Connection successful! ✅"
        )

        # ----------------------------------------------------
        # Test SQL query
        # ----------------------------------------------------

        cursor = connection.cursor()

        cursor.execute(
            "SELECT version();"
        )

        result = cursor.fetchone()

        print()
        print("PostgreSQL version:")
        print(result[0])

        # ----------------------------------------------------
        # Close connection
        # ----------------------------------------------------

        cursor.close()
        connection.close()

        print()
        print(
            "[POSTGRES] Connection closed."
        )

    except Exception as error:

        print()
        print(
            "[POSTGRES] Connection failed ❌"
        )

        print(
            f"Error: {error}"
        )


if __name__ == "__main__":
    main()