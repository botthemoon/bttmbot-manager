import threading
import time
from typing import Optional

from src.services.logger import logger
from src.services.threadmanager.config import INITIALIZED, NOCANCELSTATES, CANCELLED, COMPLETED, RUNNING
from src.services.threadmanager.thread_exceptions import WaitTimeout, CancelledError, BadStateError
from src.services.threadmanager.thread_utils import get_func_name, thread_func_tag


class TimedThread(threading.Thread):
    """
    A thread that tracks start and completion times for statistics.
    There are some API similarities to Future objects to simplify other parts of this package.
    """

    def __init__(self, master: 'ThreadPoolWrapper' = None, pool: 'ThreadPool' = None, group=None, tag: str = "",
                 target=None, name=None, args=(), kwargs=None, safe=True):
        """Initialize a thread with added 'safe' boolean parameter. When True, exceptions will be caught."""
        super().__init__(group=group, target=target, name=name, args=args, kwargs=kwargs)
        self._rlock = threading.RLock()
        self._condition = threading.Condition(self._rlock)
        self._args = args
        self._kwargs = (kwargs if kwargs else {})
        self._exception = None
        self._func_name = get_func_name(target)
        self._master = master
        self._pool = pool
        self._result = None
        self._safe = safe
        self._state = INITIALIZED
        self._tag = tag
        self._target = target
        self._time_started: float = 0.0
        self._time_completed: float = 0.0

    def cancel(self) -> bool:
        """
        Attempt to cancel the run of the thread.
        :return: bool True if successful
        """
        with self._condition:
            if self._state in NOCANCELSTATES:
                return False
            else:
                self._state = CANCELLED
                self._time_started = self._time_completed = time.time()
                self._notify_master(cancelled=True)
                return True

    def cancelled(self) -> bool:
        """True when the thread was cancelled"""
        with self._condition:
            return self._state == CANCELLED

    def current_runtime(self) -> float:
        """Return the time since start. Returns total runtime if already finished running."""
        if self._state == INITIALIZED:
            raise RuntimeError("current_runtime called before TimedThread started")
        elif self.done():
            return self.total_runtime()
        else:
            return time.time() - self._time_started

    def done(self) -> bool:
        """True when the thread was cancelled or completed"""
        with self._condition:
            return self._state in (CANCELLED, COMPLETED)

    def exception(self, timeout: float = None) -> Optional[Exception]:
        """
        Gets the exception (if any) that resulted from running the target function
        :param timeout: float number of seconds to wait for thread completion
        :raises: WaitTimeout if the thread is not completed by the timeout provided
        """
        with self._condition:
            if self.done():
                return self._exception
            else:
                self._condition.wait(timeout)

                if self.done():
                    return self._exception
                else:
                    raise WaitTimeout

    @property
    def func_name(self) -> str:
        """Name of the function the thread is supposed to run"""
        return self._func_name

    def result(self, timeout: float = None):
        """
        Get the result of the function run in the thread. If there was an exception, it is raised.
        :param timeout: float number of seconds to wait for the result
        :raises: CancelledError if the thread was cancelled
        :raises: WaitTimeout if a timeout was provided and result was not ready on time
        """
        with self._condition:
            if self.done():
                if self._exception:
                    raise self._exception
                elif self.cancelled():
                    raise CancelledError(f"TimedThread ({thread_func_tag(self)}) was cancelled")
                return self._result
            else:
                self._condition.wait(timeout)

                if self.done():
                    if self._exception:
                        raise self._exception
                    elif self.cancelled():
                        raise CancelledError(f"TimedThread ({thread_func_tag(self)}) was cancelled")
                    return self._result
                else:
                    raise WaitTimeout

    def run(self):
        """Internal function called when the thread starts"""
        with self._condition:
            if self._state == INITIALIZED:
                self._state = RUNNING
                self._time_started = time.time()
            elif self._state == CANCELLED:
                self._condition.notify_all()
                return  # master was notified in cancel method and times were stored.
            else:
                raise BadStateError("TimedThread is not in expected state in run method")
        try:
            result = self._target(*self._args, **self._kwargs)
        except BaseException as E:
            logger.exception(f"TimedThread ({thread_func_tag(self)}) ended with an exception!")
            if self._safe:
                with self._condition:
                    self._exception = E
            else:
                raise
        else:
            with self._condition:
                self._result = result
        finally:
            with self._condition:
                self._time_completed = time.time()
                self._state = COMPLETED
            self._notify_master()

    def running(self) -> bool:
        """Whether or not the thread is currently executing"""
        with self._condition:
            return self._state == RUNNING

    @property
    def tag(self) -> str:
        """The tag that was passed to ThreadManager.add()"""
        return self._tag

    @property
    def time_started(self) -> float:
        """The time the thread was either started or cancelled"""
        with self._condition:
            return self._time_started

    def total_runtime(self, timeout: float = None) -> float:
        """
        Get the total time in seconds that it took to complete the threaded function.
        This will block until that completion or until a timeout, if one is specified.
        :param timeout: float for seconds to wait for result
        :return: float number of seconds
        """
        with self._condition:
            if self.done():
                return self._time_completed - self._time_started
            else:
                self._condition.wait(timeout)

                if self.done():
                    return self._time_completed - self._time_started
                else:
                    raise WaitTimeout

    def _notify_master(self, cancelled: bool = False):
        """
        Notify the master ThreadPoolWrapper that we've either completed or have been cancelled.
        This should only be called from .run() as it means the thread was actually started.
        """
        with self._condition:
            # Release all threads that are waiting on exception or result, etc.
            self._condition.notify_all()
        if self._master:
            self._master.discard_thread(self)
            self._pool.queue_check(cancelled=cancelled)
