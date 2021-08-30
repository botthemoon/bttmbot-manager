import time
from typing import Callable

from src.services.logger import logger
from src.services.threadmanager.config import DEFAULT_CALLBACK_EXCESSIVE_BLOCK_TIME, MAX_CALLBACK_EXCESSIVE_BLOCK_TIME
from src.services.threadmanager.thread_utils import get_func_name


class Callback(object):
    def __init__(self, removal_cb: Callable, callback_type: str, func: Callable, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self._func = func
        self._removal_cb = removal_cb
        self._type = callback_type
        self._warning_block_time = DEFAULT_CALLBACK_EXCESSIVE_BLOCK_TIME
        logger.debug(f"adding {self._type} callback for {get_func_name(self._func)}")

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self._type, self._func)

    def remove(self):
        logger.debug(f"removing {self._type} callback for {get_func_name(self._func)}")
        self._removal_cb(self)

    def run(self):
        start_time = time.perf_counter()
        try:
            self._func(*self._args, **self._kwargs)
        except Exception:
            logger.exception(f"Exception in {self._type} callback! func: {get_func_name(self._func)}")
        total_time = time.perf_counter() - start_time
        if total_time >= self._warning_block_time:
            logger.warning(
                f"callback for {get_func_name(self._func)} took longer than {self._warning_block_time} seconds"
            )

    def set_warning_block_time(self, seconds: float):
        """Override the amount of time at which excessive blocking by this callback is logged"""
        if isinstance(seconds, float):
            if seconds <= 0:
                raise ValueError(f"seconds must be greater than 0, got {seconds}")
            elif seconds > MAX_CALLBACK_EXCESSIVE_BLOCK_TIME:
                raise ValueError(f"seconds can not be greater than {MAX_CALLBACK_EXCESSIVE_BLOCK_TIME}, got {seconds}")
            else:
                self._warning_block_time = seconds
        else:
            raise ValueError(f"Expected float, got '{type(seconds)}'")

    @property
    def type(self):
        return self._type
