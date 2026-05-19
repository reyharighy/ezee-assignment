import os
from typing import Literal, TypedDict, Unpack

from groq import BadRequestError
from langchain_core.runnables import Runnable
from langchain_groq import ChatGroq

from app.config import get_settings

language_model_cfg = get_settings().language_model

class ModelKwargs(TypedDict, total=False):
    model: str
    temperature: int | float
    max_tokens: int | None
    reasoning_format: Literal["parsed", "raw", "hidden"]
    reasoning_effort: Literal["low", "medium", "high"]


def with_retry_exception(runnable: Runnable) -> Runnable:
    return runnable.with_retry(retry_if_exception_type=(BadRequestError,))


def get_language_model(**kwargs: Unpack[ModelKwargs]):
    model = kwargs.get("model", "openai/gpt-oss-20b")
    temperature = float(kwargs.get("temperature", 0))
    max_tokens = kwargs.get("max_tokens", None)
    reasoning_format = kwargs.get("reasoning_format", "parsed")
    reasoning_effort = kwargs.get("reasoning_effort", "low")

    llm = ChatGroq(
        api_key=language_model_cfg.api_key,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        reasoning_format=reasoning_format,
        reasoning_effort=reasoning_effort,
        timeout=None,
    )

    return llm
