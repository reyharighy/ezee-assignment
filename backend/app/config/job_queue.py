from typing import Annotated

from pydantic import BeforeValidator, Field
from pydantic_settings import BaseSettings

from .settings_env import model_config

JOB_QUEUE_RESULT_TTL_DEFAULT = -1


def parse_url(value: str) -> str:
    if value.strip() == "":
        raise ValueError("JOB_QUEUE_URL is not set")

    return value.strip()


def parse_result_ttl(value: str) -> str:
    if value.strip() == "":
        return str(JOB_QUEUE_RESULT_TTL_DEFAULT)

    if int(value.strip()) <= 0 and not value.strip() == "-1":
        raise ValueError("JOB_QUEUE_RESULT_TTL must be a positive number or -1")

    return value.strip()


Url = Annotated[str, BeforeValidator(parse_url)]
ResultTtl = Annotated[str, BeforeValidator(parse_result_ttl)]


class JobQueueConfig(BaseSettings):
    model_config = model_config(
        env_prefix="JOB_QUEUE_",
    )

    url: Url = Field(
        exclude=True,
        description="URL of the job queue service",
    )

    result_ttl: ResultTtl = Field(
        exclude=True,
        default="",
        description="TTL of the job queue result in seconds (-1 = forever)",
    )

    @property
    def url_optioned(self) -> str:
        return self.url

    @property
    def result_ttl_optioned(self) -> int:
        if self.result_ttl == "-1":
            return -1

        return int(self.result_ttl)
