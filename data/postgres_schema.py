"""
Machine Doctor PostgreSQL database schema.

Creates the core relational tables used by the platform.
"""

import os

import pg8000
from dotenv import load_dotenv


load_dotenv()


def get_connection():

    return pg8000.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        database=os.getenv(
            "POSTGRES_DB",
            "ai_machine_doctor",
        ),
        user=os.getenv(
            "POSTGRES_USER",
            "postgres",
        ),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def create_tables():

    connection = get_connection()
    cursor = connection.cursor()

    print()
    print("=" * 60)
    print("       MACHINE DOCTOR - DATABASE SETUP")
    print("=" * 60)
    print()

    # ========================================================
    # 1. MACHINES
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS machines (

            machine_id VARCHAR(100) PRIMARY KEY,

            machine_name VARCHAR(200),

            machine_type VARCHAR(100),

            plant_id VARCHAR(100),

            status VARCHAR(50),

            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP

        );
        """
    )

    print("[POSTGRES] machines table ready.")

    # ========================================================
    # 2. MACHINE EVENTS
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS machine_events (

            event_id UUID PRIMARY KEY,

            machine_id VARCHAR(100) NOT NULL,

            event_type VARCHAR(100) NOT NULL,

            message TEXT,

            timestamp TIMESTAMPTZ NOT NULL,

            metadata JSONB DEFAULT '{}'::jsonb,

            FOREIGN KEY (machine_id)
                REFERENCES machines(machine_id)

        );
        """
    )

    print("[POSTGRES] machine_events table ready.")

    # ========================================================
    # 3. MACHINE ALARMS
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS machine_alarms (

            alarm_id UUID PRIMARY KEY,

            machine_id VARCHAR(100) NOT NULL,

            code VARCHAR(100) NOT NULL,

            severity VARCHAR(50) NOT NULL,

            message TEXT,

            timestamp TIMESTAMPTZ NOT NULL,

            acknowledged BOOLEAN DEFAULT FALSE,

            acknowledged_by VARCHAR(100),

            acknowledged_at TIMESTAMPTZ,

            FOREIGN KEY (machine_id)
                REFERENCES machines(machine_id)

        );
        """
    )

    print("[POSTGRES] machine_alarms table ready.")

    # ========================================================
    # 4. MAINTENANCE RECORDS
    # ========================================================

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS maintenance_records (

            maintenance_id UUID PRIMARY KEY,

            machine_id VARCHAR(100) NOT NULL,

            maintenance_type VARCHAR(100),

            description TEXT,

            performed_by VARCHAR(200),

            performed_at TIMESTAMPTZ,

            next_due_at TIMESTAMPTZ,

            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (machine_id)
                REFERENCES machines(machine_id)

        );
        """
    )

    print(
        "[POSTGRES] maintenance_records table ready."
    )

    # ========================================================
    # Commit
    # ========================================================

    connection.commit()

    cursor.close()
    connection.close()

    print()
    print("=" * 60)
    print("DATABASE SETUP COMPLETE ✅")
    print("=" * 60)


if __name__ == "__main__":
    create_tables()