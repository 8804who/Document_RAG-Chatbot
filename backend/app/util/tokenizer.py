
import tiktoken

from app.core.config import settings


class Tokenizer:
    def __init__(self, model: str):
        self.model = model
        self.tokenizer = tiktoken.encoding_for_model(model)

    def count_tokens(self, text) -> int:
        """
        토큰 수 계산

        Args:
            text: 토큰 수를 계산할 텍스트 (str 또는 message 객체)

        Returns:
            int: 토큰 수
        """
        # Handle different input types
        if isinstance(text, str):
            text_content = text
        elif hasattr(text, "content"):
            text_content = text.content
        elif hasattr(text, "text"):
            text_content = text.text
        else:
            text_content = str(text)

        # Ensure we have a string
        if not isinstance(text_content, str):
            text_content = str(text_content)

        return len(self.tokenizer.encode(text_content))


class OpenAiTokenizer(Tokenizer):
    def __init__(self):
        super().__init__(settings.OPENAI_MODEL)


class AnthropicTokenizer(Tokenizer):
    def __init__(self):
        super().__init__(settings.ANTHROPIC_MODEL)


class GoogleVertexAiTokenizer(Tokenizer):
    def __init__(self):
        super().__init__(settings.GOOGLE_MODEL)


class HuggingFaceTokenizer(Tokenizer):
    def __init__(self):
        super().__init__(settings.HUGGING_FACE_TOKENIZER)
