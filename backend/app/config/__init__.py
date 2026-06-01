from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings

from .database import DatabaseConfig
from .embedding import EmbeddingConfig
from .health_check import HealthCheckConfig
from .job_queue import JobQueueConfig
from .middleware import MiddlewareConfig
from .language_model import LanguageModelConfig
from .settings_env import settings_default_factory


class Settings(BaseSettings):
    database: DatabaseConfig = Field(
        default_factory=settings_default_factory(DatabaseConfig),
        description="Database configuration",
    )

    embedding: EmbeddingConfig = Field(
        default_factory=settings_default_factory(EmbeddingConfig),
        description="Embedding configuration",
    )

    health_check: HealthCheckConfig = Field(
        default_factory=settings_default_factory(HealthCheckConfig),
        description="Health check configuration",
    )

    job_queue: JobQueueConfig = Field(
        default_factory=settings_default_factory(JobQueueConfig),
        description="Job queue configuration",
    )

    language_model: LanguageModelConfig = Field(
        default_factory=settings_default_factory(LanguageModelConfig),
        description="Language model configuration",
    )

    middleware: MiddlewareConfig = Field(
        default_factory=settings_default_factory(MiddlewareConfig),
        description="Middleware configuration",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
