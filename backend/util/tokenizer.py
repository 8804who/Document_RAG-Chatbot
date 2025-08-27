from core import config

import time
import tiktoken


class Tokenizer:
    def __init__(self, model: str):
        self.model = model
        self.tokenizer = tiktoken.encoding_for_model(model)

    def count_tokens(self, text: str) -> int:
        """
        토큰 수 계산

        Args:
            text (str): 토큰 수를 계산할 텍스트

        Returns:
            int: 토큰 수
        """
        return len(self.tokenizer.encode(text))


class OpenAiTokenizer(Tokenizer):
    def __init__(self):
        super().__init__(config.OPENAI_MODEL)


class AnthropicTokenizer(Tokenizer):
    def __init__(self):
        super().__init__(config.ANTHROPIC_MODEL)


class GoogleVertexAiTokenizer(Tokenizer):
    def __init__(self):
        super().__init__(config.GOOGLE_MODEL)


class HuggingFaceTokenizer(Tokenizer):
    def __init__(self):
        super().__init__(config.HUGGING_FACE_TOKENIZER)