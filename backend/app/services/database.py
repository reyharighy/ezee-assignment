from functools import lru_cache
import psycopg
from psycopg.rows import TupleRow
from langchain_postgres import PGEngine


@lru_cache(maxsize=1)
def get_engine(url: str) -> PGEngine:
    return PGEngine.from_connection_string(url)


@lru_cache(maxsize=1)
def get_psycopg_connection(url: str) -> psycopg.Connection[TupleRow]:
    for prefix in ("postgresql+psycopg://",):
        if url.startswith(prefix):
            return psycopg.connect(f"postgresql://{url[len(prefix) :]}")

    return psycopg.connect(url)
