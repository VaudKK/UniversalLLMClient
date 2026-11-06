import httpx
import pytest
import respx


OPENAI_URL = "https://api.openai.com/v1/responses"

@pytest.mark.asyncio
async def test_generate_returns_normalized_response(llm_client):

    mock_response = mock_response = {
        "id": "resp_test123",
        "object": "response",
        "created_at": 1760000000,
        "status": "completed",
        "error": None,
        "incomplete_details": None,
        "instructions": None,
        "max_output_tokens": 1000,
        "model": "test-model",
        "output": [
            {
                "id": "msg_test123",
                "type": "message",
                "status": "completed",
                "role": "assistant",
                "content": [
                    {
                        "type": "output_text",
                        "text": "Dependency injection is a design pattern.",
                        "annotations": [],
                    }
                ],
            }
        ],
        "parallel_tool_calls": True,
        "temperature": 1.0,
        "tool_choice": "auto",
        "tools": [],
        "top_p": 1.0,
        "usage": {
            "input_tokens": 20,
            "output_tokens": 12,
            "total_tokens": 32,
        },
    }


    with respx.mock:
        route = respx.post(OPENAI_URL).mock(
            return_value=httpx.Response(
                status_code=200,
                json=mock_response,
                headers={"x-request-id": "req_test123"},
            )
        )


        try:
            result = await llm_client.generate(
                prompt = "Explain dependency injection in simple terms.",
            )

            assert route.called

            assert result.content == "Dependency injection is a design pattern."

            assert result.provider == "openai"
            assert result.model == "test-model"

            #verify token usage
            assert result.usage.input_tokens == 20
            assert result.usage.output_tokens == 12
            assert result.usage.total_tokens == 32

        finally:
            await llm_client.close()