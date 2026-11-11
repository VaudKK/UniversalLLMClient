import asyncio


from universal_llm_client.observability import logger


from universal_llm_client import (
    LLMClient,
    LLMSettings,
    AnthropicProvider,
)


async def main():
    settings = LLMSettings()
    provider = AnthropicProvider(settings)
    client = LLMClient(provider)

    try:
        
        response = await client.generate(
             prompt = "Explain the theory of relativity in simple terms.",
        )
        
        print(response)

        # async for chunk in client.stream(
        #     prompt = "Explain the theory of relativity in simple terms.",
        # ):
        #     print(chunk, end="", flush=True)


    finally:
        await client.close()



if __name__ == "__main__":
    asyncio.run(main())