from data.postgres_writer import PostgreSQLWriter


def main():

    writer = PostgreSQLWriter()

    writer.connect()

    writer.ensure_machine(
        "MACHINE_001"
    )

    writer.close()


if __name__ == "__main__":
    main()