import logging
from typing import Type


def log_and_raise(msg: str, exc_type: Type[Exception]):
    logging.error(msg)
    raise exc_type(msg)
