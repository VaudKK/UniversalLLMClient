from typing import Callable, ParamSpec, TypeVar

from openai import APIConnectionError, APITimeoutError, InternalServerError, RateLimitError
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_random_exponential


P = ParamSpec("P")
T = TypeVar("T")

def with_retry(func: Callable[P, T]) -> Callable[P, T]:
    return retry(
        retry = retry_if_exception_type(
            (
                APIConnectionError,
                APITimeoutError,
                RateLimitError,
                InternalServerError,
            )
        ),
        wait = wait_random_exponential(
            multiplier = 1,
            max = 20,
        ),
        stop = stop_after_attempt(3),
        reraise = True,

    )(func)