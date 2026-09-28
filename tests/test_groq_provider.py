from llm.groq_provider import (
    GroqProvider,
)


def main():

    print()
    print("=" * 60)
    print(" MACHINE DOCTOR - GROQ LLM TEST")
    print("=" * 60)

    provider = GroqProvider()

    print()
    print(
        f"Model: {provider.model}"
    )

    print()
    print("Sending test request...")

    response = provider.generate(

        system_prompt=(
            "You are Machine Doctor, "
            "an industrial machine intelligence assistant."
        ),

        user_prompt=(
            "Explain in one short paragraph "
            "why machine temperature monitoring "
            "is useful."
        ),
    )

    print()
    print("LLM Response")
    print("-" * 60)

    print(response)

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()