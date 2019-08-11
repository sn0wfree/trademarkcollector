# coding=utf8
import logging
from functools import wraps


def use_logging(level):
    def decorator(func):
        @wraps
        def wrapper(*args, **kwargs):
            if level == "warning":
                logging.warning("%s is running" % func.__name__)
            elif level == "info":
                logging.info("%s is running" % func.__name__)
            elif level == "debug":
                logging.debug("%s is running" % func.__name__)
            return func(*args, **kwargs)

        return wrapper

    return decorator
