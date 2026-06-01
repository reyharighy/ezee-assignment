from typing import Annotated

from pydantic import BeforeValidator, Field, computed_field
from pydantic_settings import BaseSettings

from .settings_env import model_config


HEALTH_PROVIDER_CACHE_TTL_DEFAULT = 300


def parse_provider_cache_ttl(value: str) -> str:
    if value.strip() == "":
        return str(HEALTH_PROVIDER_CACHE_TTL_DEFAULT)

    if int(value.strip()) <= 0:
        raise ValueError("HEALTH_CHECK_PROVIDER_CACHE_TTL must be a positive number")

    return value.strip()

ProviderCacheTtl = Annotated[str, BeforeValidator(parse_provider_cache_ttl)]


class HealthCheckConfig(BaseSettings):
    model_config = model_config(
        env_prefix="HEALTH_CHECK",
    )

    _provider_cache_ttl: ProviderCacheTtl = Field(
        default="",
        description="TTL of the provider cache in seconds",
    )

    @computed_field
    @property
    def provider_cache_ttl(self) -> int:
        return int(self._provider_cache_ttl)