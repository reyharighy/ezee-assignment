from typing import Annotated

from pydantic import BeforeValidator, Field, SecretStr
from pydantic_settings import BaseSettings

from .settings_env import model_config


def parse_api_key(value: str) -> str:
    if value.strip() == "":
        raise ValueError("GROQ_API_KEY is not set")

    return value.strip()


ApiKey = Annotated[str, BeforeValidator(parse_api_key)]


class LanguageModelConfig(BaseSettings):
    model_config = model_config()

    api_key: ApiKey = Field(
        exclude=True,
        validation_alias="GROQ_API_KEY",
        description="API key for the language model",
    )

    @property
    def api_key_optioned(self) -> SecretStr:
        return SecretStr(self.api_key)
