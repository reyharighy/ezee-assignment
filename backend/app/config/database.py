from functools import lru_cache
from typing import Annotated

import psycopg
from psycopg.rows import TupleRow
from pydantic import BeforeValidator, Field, computed_field
from pydantic_settings import BaseSettings
from langchain_postgres import PGEngine

from .settings_env import model_config


def parse_username(value: str) -> str:
    if value.strip() == "":
        raise ValueError("DATABASE_USERNAME is not set")

    return value


def parse_password(value: str) -> str:
    if value.strip() == "":
        raise ValueError("DATABASE_PASSWORD is not set")

    return value


def parse_name(value: str) -> str:
    if value.strip() == "":
        raise ValueError("DATABASE_NAME is not set")

    return value


@lru_cache(maxsize=1)
def _get_url(username: str, password: str, name: str) -> str:
    return f"postgresql+psycopg://{username}:{password}@database:5432/{name}"


@lru_cache(maxsize=1)
def _get_engine(url: str) -> PGEngine:
    return PGEngine.from_connection_string(url)


@lru_cache(maxsize=1)
def _get_psycopg_connection(url: str) -> psycopg.Connection[TupleRow]:
    for prefix in ("postgresql+psycopg://",):
        if url.startswith(prefix):
            return psycopg.connect(f"postgresql://{url[len(prefix) :]}")

    return psycopg.connect(url)


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

    @computed_field
    @property
    def url(self) -> str:
        return _get_url(self.username, self.password, self.name)

    @computed_field
    @property
    def engine(self) -> PGEngine:
        return _get_engine(self.url)

    @computed_field
    @property
    def psycopg_connection(self) -> psycopg.Connection[TupleRow]:
        return _get_psycopg_connection(self.url)
