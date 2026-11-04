import asyncio
import time


from universal_llm_client.observability import logger


from universal_llm_client import (
    LLMClient,
    LLMSettings,
    OpenAIProvider
)


async def main():
    settings = LLMSettings()
    provider = OpenAIProvider(settings)
    client = LLMClient(provider)

    try:

        response = await client.generate(
            prompt = "Explain Go goroutines to a Java developer.",
            system_instruction = (
                "You are a senior backend engineer."
            ),
        )

        print(response.content)


    finally:
        await client.close()



if __name__ == "__main__":
    asyncio.run(main())