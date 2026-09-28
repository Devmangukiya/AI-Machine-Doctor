from intelligence.oee.oee_engine import (
    OEEEngine,
    OEEInputs,
)


def main():

    engine = OEEEngine()

    inputs = OEEInputs(

        # 8 hour production shift
        planned_production_time_s=8 * 60 * 60,

        # Machine actually ran for 7 hours
        run_time_s=7 * 60 * 60,

        # Ideal machine cycle
        ideal_cycle_time_s=4.0,

        # Production
        total_count=5500,

        # Good products
        good_count=5400,
    )

    result = engine.calculate(inputs)

    print()
    print("=" * 60)
    print("           MACHINE DOCTOR - OEE")
    print("=" * 60)

    print()

    print(
        f"Availability : "
        f"{result.availability * 100:.2f}%"
    )

    print(
        f"Performance  : "
        f"{result.performance * 100:.2f}%"
    )

    print(
        f"Quality      : "
        f"{result.quality * 100:.2f}%"
    )

    print()

    print(
        f"OEE          : "
        f"{result.oee * 100:.2f}%"
    )

    print()

    print("=" * 60)


if __name__ == "__main__":
    main()