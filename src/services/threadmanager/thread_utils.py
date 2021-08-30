import inspect

from typing import Callable


def get_caller(filepath: bool = False) -> str:
    """Return the name of the caller's caller. If filepath is True, also print the full filepath and line number"""
    current_frame = inspect.currentframe()
    if current_frame:
        caller_code = current_frame.f_back.f_back.f_code
        if filepath:
            caller = f"{caller_code.co_name} at '{caller_code.co_filename}', line {caller_code.co_firstlineno}"
        else:
            caller = caller_code.co_name
        del current_frame, caller_code
        return caller
    else:
        return "<unknown>"


def get_func_name(func: Callable) -> str:
    return func.__qualname__ if hasattr(func, '__qualname__') else '<unknown function>'


def pluralize(count: int) -> str:
    """Convenience function used to place an 's' at the end of a word when needed"""
    if count == 1:
        return ""
    else:
        return "s"


def print_valid(prefix: str, item: str):
    """
    Used to return a string if not null, with optional prefix
    :param prefix: str optional item to place before the item if it is not null
    :param item: item to return if not null
    :return: str
    """
    if item:
        return f"{prefix}{item}"
    else:
        return ""


def print_tag(tag: str) -> str:
    """Used to shorten the code in places where nothing should be printed if tag is empty"""
    return print_valid(" tag: ", tag)


def thread_func_tag(thread_item) -> str:
    """
    Convenience function to shorten printing the function name and tag (when present) associated with a thread object
    :param thread_item: Union[TimedThread, TimedFuture]
    :return: str
    """
    return f"func: {thread_item.func_name}{print_tag(thread_item.tag)}"


def thread_nametag(thread_item) -> str:
    """
    Convenience function to shorten printing the name and tag (when present) associated with a thread object
    :param thread_item: Union[TimedThread, TimedFuture]
    :return: str
    """
    return f"{thread_item.name}{print_tag(thread_item.tag)}"
