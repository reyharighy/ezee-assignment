import os
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field, SecretStr

def parse_api_key(value: str) -> SecretStr:
    if value.strip() == "":
        raise ValueError("GROQ_API_KEY is not set")

    return SecretStr(value.strip())

ApiKey = Annotated[SecretStr, BeforeValidator(parse_api_key)]

class LanguageModelConfig(BaseModel):
    api_key: ApiKey = Field(
        default_factory=lambda: os.getenv("GROQ_API_KEY", ""),
        validate_default=True,
        description="API key for the language model",
    )
