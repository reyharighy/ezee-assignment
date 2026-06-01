from typing import Annotated

from functools import lru_cache
from pydantic import BeforeValidator, Field, computed_field
from pydantic_settings import BaseSettings
from langchain_cohere import CohereEmbeddings
from langchain_core.embeddings import Embeddings

from .settings_env import model_config

ALLOWED_EMBEDDING_MODELS = [
    "embed-multilingual-v3.0",
]

ALLOWED_VECTOR_EMBEDDING_DIMENSION_DEFAULT = [
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
        return str(ALLOWED_VECTOR_EMBEDDING_DIMENSION_DEFAULT[2])

    if int(value.strip()) in ALLOWED_VECTOR_EMBEDDING_DIMENSION_DEFAULT:
        return value.strip()

    raise ValueError(
        "EMBEDDING_DIMENSION must be one of the following: "
        + ", ".join(map(str, ALLOWED_VECTOR_EMBEDDING_DIMENSION_DEFAULT))
    )


def parse_api_key(value: str) -> str:
    if value.strip() == "":
        raise ValueError("COHERE_API_KEY is not set")

    return value.strip()


@lru_cache(maxsize=1)
def _get_embedding_service(api_key: "ApiKey", model: "Model") -> Embeddings:
    return CohereEmbeddings(
        cohere_api_key=api_key,
        model=model,
    )  # type: ignore


Model = Annotated[str, BeforeValidator(parse_model)]
Dimension = Annotated[str, BeforeValidator(parse_dimension)]
ApiKey = Annotated[str, BeforeValidator(parse_api_key)]


class EmbeddingConfig(BaseSettings):
    model_config = model_config(
        env_prefix="EMBEDDING",
        arbitrary_types_allowed=True
    )

    _model: Model = Field(
        default="",
        description="Model of the embedding service"
    )

    _dimension: Dimension = Field(
        default="",
        description="Dimension of stored embedding vectors"
    )

    _api_key: ApiKey = Field(
        validation_alias="COHERE_API_KEY",
        description="API key of the embedding service",
    )

    @computed_field
    @property
    def model(self) -> str:
        return self._model

    @computed_field
    @property
    def dimension(self) -> int:
        return int(self._dimension)

    @computed_field
    @property
    def service(self) -> Embeddings:
        return _get_embedding_service(self._api_key, self._model)
