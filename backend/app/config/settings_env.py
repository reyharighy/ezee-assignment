from pathlib import Path
from typing import Any, Callable, TypeVar

from pydantic_settings import SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = REPO_ROOT / ".env"

T = TypeVar("T")


def model_config(**overrides: Any) -> SettingsConfigDict:
    return SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
        **overrides,
    )


def settings_default_factory(model: type[T]) -> Callable[[], T]:
    def factory() -> T:
        return model()  # type: ignore[call-arg]

    return factory
