"""
Machine Doctor - Groq LLM Provider

Provider layer for Groq-hosted LLMs.

The rest of Machine Doctor should not need to know
which LLM provider is being used.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-20b",
)


class GroqProvider:

    def __init__(self):

        if not GROQ_API_KEY:

            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=GROQ_API_KEY,
            base_url=(
                "https://api.groq.com/openai/v1"
            ),
        )

        self.model = GROQ_MODEL

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        response = (
            self.client.responses.create(

                model=self.model,

                instructions=system_prompt,

                input=user_prompt,
            )
        )

        return response.output_text