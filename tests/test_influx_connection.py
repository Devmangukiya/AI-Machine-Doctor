import os

from dotenv import load_dotenv
from influxdb_client import InfluxDBClient


load_dotenv()


URL = os.getenv(
    "INFLUXDB_URL",
    "http://localhost:8086",
)

TOKEN = os.getenv("INFLUXDB_TOKEN")

ORG = os.getenv(
    "INFLUXDB_ORG"
)


def main():

    print()
    print("=" * 60)
    print("        INFLUXDB CONNECTION CHECK")
    print("=" * 60)

    print()
    print("URL :", URL)
    print("ORG :", ORG)

    client = InfluxDBClient(
        url=URL,
        token=TOKEN,
        org=ORG,
    )

    buckets_api = client.buckets_api()

    buckets = buckets_api.find_buckets()

    print()
    print("Buckets visible to this token:")
    print()

    for bucket in buckets.buckets:

        print(
            f"- {bucket.name}"
        )

    client.close()

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()