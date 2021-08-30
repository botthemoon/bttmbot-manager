import concurrent
import time
from typing import Optional

from src.services.logger import logger
from src.services.threadmanager.thread_utils import get_func_name, thread_func_tag


class TimedFuture(concurrent.futures.Future):
    def __init__(self, func_name: str, runtime_alert: float, tag: str = ""):
        super().__init__()
        self._func_name = func_name
        self._runtime_alert = runtime_alert
        self._tag = tag
        self._time_started: float = 0.0
        self._time_completed: float = 0.0

    def current_runtime(self) -> float:
        """Return the time since start. Returns total runtime if already finished running."""
        if self._state == concurrent.futures._base.PENDING:
            raise RuntimeError("current_runtime called before TimedFuture started")
        elif self.done():
            return self.total_runtime()
        else:
            return time.time() - self._time_started

    @property
    def func_name(self):
        return self._func_name

    name = func_name

    def set_exception(self, exception):
        with self._condition:
            self._set_time_completed()
            logger.exception(f"TimedFuture ({thread_func_tag(self)}) ended with an exception!")
            super().set_exception(exception)

    def set_result(self, result):
        with self._condition:
            self._set_time_completed()
            super().set_result(result)

    def set_running_or_notify_cancel(self) -> bool:
        with self._condition:
            self._time_started = time.time()
            if super().set_running_or_notify_cancel() is False:
                # Future was cancelled
                self._set_time_completed()
                return False
            else:
                return True

    @property
    def tag(self):
        return self._tag

    @property
    def time_started(self):
        with self._condition:
            return self._time_started

    def total_runtime(self, timeout: Optional[float] = None) -> float:
        with self._condition:
            if self.done():
                return self._time_completed - self._time_started
            else:
                self._condition.wait(timeout)

                if self.done():
                    return self._time_completed - self._time_started
                else:
                    raise concurrent.futures.TimeoutError()

    def _set_time_completed(self):
        with self._condition:
            self._time_completed = time.time()


class TimedFutureThreadPool(concurrent.futures.ThreadPoolExecutor):
    def __init__(self, master: 'ThreadPoolWrapper', *args, runtime_alert: float = 0.0, **kwargs):
        import warnings
        msg = "ThreadPoolExecutor will be removed in 1.0.0 - please use the default pool_type instead for add_pool()"
        warnings.warn(msg, FutureWarning)
        logger.critical(msg)
        super().__init__(*args, **kwargs)
        self._master = master
        self.runtime_alert = runtime_alert

    def submit(self, tag: str, fn, *args, **kwargs):
        # Over-ridden to use TimedFuture instead
        with self._shutdown_lock:
            if self._shutdown:
                raise RuntimeError("cannot schedule new futures after shutdown")

            f = TimedFuture(get_func_name(fn), self.runtime_alert, tag=tag)
            w = concurrent.futures.thread._WorkItem(f, fn, args, kwargs)

            f.add_done_callback(self._master.discard_thread)

            self._master.track_thread(f)
            self._work_queue.put(w)
            self._adjust_thread_count()
            return f

    @property
    def worker_count(self):
        return self._max_workers

    @worker_count.setter
    def worker_count(self, value: int):
        raise NotImplementedError("On-the-fly worker count adjustment has not been implemented for Future-based pools")
