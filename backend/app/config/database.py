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


def parse_database_name(value: str) -> str:
    if value.strip() == "":
        raise ValueError("DATABASE_NAME is not set")

    return value

def _get_database_url(username: str, password: str, name: str) -> str:
    return f"postgresql+psycopg://{username}:{password}@database:5432/{name}"

@lru_cache(maxsize=1)
def _get_engine(database_url: str) -> PGEngine:
    return PGEngine.from_connection_string(database_url)


@lru_cache(maxsize=1)
def _get_psycopg_connection(database_url: str) -> psycopg.Connection[TupleRow]:
    for prefix in ("postgresql+psycopg://",):
        if database_url.startswith(prefix):
            return psycopg.connect(f"postgresql://{database_url[len(prefix) :]}")

    return psycopg.connect(database_url)


UserName = Annotated[str, BeforeValidator(parse_username)]
Password = Annotated[str, BeforeValidator(parse_password)]
DatabaseName = Annotated[str, BeforeValidator(parse_database_name)]


class DatabaseConfig(BaseSettings):
    model_config = model_config(
        env_prefix="DATABASE",
        arbitrary_types_allowed=True,
    )

    _username: UserName = Field(description="Username for the database")
    _password: Password = Field(description="Password for the database")
    _name: DatabaseName = Field(description="Name of the database")

    @computed_field
    @property
    def database_url(self) -> str:
        return _get_database_url(self._username, self._password, self._name)

    @computed_field
    @property
    def engine(self) -> PGEngine:
        return _get_engine(self.database_url)

    @computed_field
    @property
    def psycopg_connection(self) -> psycopg.Connection[TupleRow]:
        return _get_psycopg_connection(self.database_url)
