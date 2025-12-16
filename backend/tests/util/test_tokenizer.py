from langchain_core.messages import BaseMessage
import pytest

from app.util.tokenizer import OpenAiTokenizer


@pytest.mark.asyncio
async def test_openai_tokenizer_count_tokens_with_string():
    tokenizer = OpenAiTokenizer()
    assert tokenizer.count_tokens("Hello, world!") == 4


@pytest.mark.asyncio
async def test_openai_tokenizer_count_tokens_with_message():
    tokenizer = OpenAiTokenizer()
    assert tokenizer.count_tokens(BaseMessage(type="human", content="Hello, world!")) == 4