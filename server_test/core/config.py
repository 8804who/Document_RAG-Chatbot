from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr
from typing import Optional


class Settings(BaseSettings):
    # Test Settings
    TEST_SCENARIO: Optional[str] = Field(None, env="TEST_SCENARIO")

    # Google OAuth
    GOOGLE_CLIENT_ID: Optional[str] = Field(None, env="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: Optional[SecretStr] = Field(None, env="GOOGLE_CLIENT_SECRET")
    GOOGLE_REFRESH_TOKEN: Optional[SecretStr] = Field(None, env="GOOGLE_REFRESH_TOKEN")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


settings = Settings()
