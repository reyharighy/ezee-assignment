from functools import lru_cache
from typing import Annotated

from pydantic import BeforeValidator, Field
from pydantic_settings import BaseSettings

from .settings_env import model_config


def parse_username(value: str) -> str:
    if value.strip() == "":
        raise ValueError("DATABASE_USERNAME is not set")

    return value.strip()


def parse_password(value: str) -> str:
    if value.strip() == "":
        raise ValueError("DATABASE_PASSWORD is not set")

    return value.strip()


def parse_name(value: str) -> str:
    if value.strip() == "":
        raise ValueError("DATABASE_NAME is not set")

    return value.strip()


@lru_cache(maxsize=1)
def _get_url(username: str, password: str, name: str) -> str:
    return f"postgresql+psycopg://{username}:{password}@database:5432/{name}"


UserName = Annotated[str, BeforeValidator(parse_username)]
Password = Annotated[str, BeforeValidator(parse_password)]
Name = Annotated[str, BeforeValidator(parse_name)]


class DatabaseConfig(BaseSettings):
    model_config = model_config(
        env_prefix="DATABASE_",
        arbitrary_types_allowed=True,
    )

    username: UserName = Field(exclude=True, description="Username for the database")
    password: Password = Field(exclude=True, description="Password for the database")
    name: Name = Field(exclude=True, description="Name of the database")

    @property
    def url(self) -> str:
        return _get_url(self.username, self.password, self.name)
