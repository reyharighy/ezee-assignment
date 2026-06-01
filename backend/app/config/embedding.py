from typing import Annotated

from functools import lru_cache
from pydantic import BeforeValidator, Field, computed_field, SecretStr
from pydantic_settings import BaseSettings
from langchain_cohere import CohereEmbeddings
from langchain_core.embeddings import Embeddings

from .settings_env import model_config

ALLOWED_EMBEDDING_MODELS = [
    "embed-multilingual-v3.0",
]

ALLOWED_EMBEDDING_DIMENSION_DEFAULT = [
    384,
    768,
    1024,
    1536,
    2048,
    3072,
]


def parse_model(value: str) -> str:
    if value.strip() == "":
        return ALLOWED_EMBEDDING_MODELS[0]

    if value.strip() in ALLOWED_EMBEDDING_MODELS:
        return value.strip()

    raise ValueError(
        "EMBEDDING_MODEL must be one of the following: "
        + ", ".join(ALLOWED_EMBEDDING_MODELS)
    )


def parse_dimension(value: str) -> str:
    if value.strip() == "":
        return str(ALLOWED_EMBEDDING_DIMENSION_DEFAULT[2])

    if int(value.strip()) in ALLOWED_EMBEDDING_DIMENSION_DEFAULT:
        return value.strip()

    raise ValueError(
        "EMBEDDING_DIMENSION must be one of the following: "
        + ", ".join(map(str, ALLOWED_EMBEDDING_DIMENSION_DEFAULT))
    )


def parse_api_key(value: str) -> str:
    if value.strip() == "":
        raise ValueError("COHERE_API_KEY is not set")

    return value.strip()


Model = Annotated[str, BeforeValidator(parse_model)]
Dimension = Annotated[str, BeforeValidator(parse_dimension)]
ApiKey = Annotated[str, BeforeValidator(parse_api_key)]


class EmbeddingConfig(BaseSettings):
    model_config = model_config(
        env_prefix="EMBEDDING_",
    )

    model: Model = Field(
        exclude=True, default="", description="Model of the embedding service"
    )

    dimension: Dimension = Field(
        exclude=True, default="", description="Dimension of stored embedding vectors"
    )

    api_key: ApiKey = Field(
        exclude=True,
        validation_alias="COHERE_API_KEY",
        description="API key of the embedding service",
    )

    @property
    def model_optioned(self) -> str:
        return self.model

    @property
    def dimension_optioned(self) -> int:
        return int(self.dimension)

    @property
    def api_key_optioned(self) -> SecretStr:
        return SecretStr(self.api_key)
