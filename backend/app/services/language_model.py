from typing import Literal, TypedDict, Unpack
from functools import lru_cache

from groq import BadRequestError
from langchain_core.language_models.base import LanguageModelInput
from langchain_core.runnables import Runnable
from langchain_groq import ChatGroq

from app.config import get_settings
from pydantic import BaseModel

language_model_cfg = get_settings().language_model


class ModelKwargs(TypedDict, total=False):
    model: str
    temperature: int | float
    max_tokens: int | None
    reasoning_format: Literal["parsed", "raw", "hidden"]
    reasoning_effort: Literal["low", "medium", "high"]


def llm_with_retry(
    runnable: Runnable[LanguageModelInput, dict | BaseModel],
) -> Runnable[LanguageModelInput, dict | BaseModel]:
    return runnable.with_retry(retry_if_exception_type=(BadRequestError,))

@lru_cache(maxsize=1)
def get_language_model(**kwargs: Unpack[ModelKwargs]):
    model = kwargs.get("model", "openai/gpt-oss-20b")
    temperature = float(kwargs.get("temperature", 0))
    max_tokens = kwargs.get("max_tokens", None)
    reasoning_format = kwargs.get("reasoning_format", "parsed")
    reasoning_effort = kwargs.get("reasoning_effort", "low")

    return ChatGroq(
        api_key=language_model_cfg.api_key_optioned,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        reasoning_format=reasoning_format,
        reasoning_effort=reasoning_effort,
        timeout=None,
    )
