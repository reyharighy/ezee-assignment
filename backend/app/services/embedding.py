from functools import lru_cache
from pydantic import SecretStr
from langchain_cohere import CohereEmbeddings
from langchain_core.embeddings import Embeddings
from app.config import get_settings

embedding_cfg = get_settings().embedding


@lru_cache(maxsize=1)
def get_embedding_service() -> Embeddings:
    return CohereEmbeddings(
        cohere_api_key=embedding_cfg.api_key_optioned.get_secret_value(),
        model=embedding_cfg.model_optioned,
    )  # type: ignore
