import time
from datetime import datetime


class Utils:

    @staticmethod
    def get_timestamp() -> int:
        return int(time.time() * 1000)

    @staticmethod
    def passed_24_hours_since(timestamp_ms):
        timestamp_s = timestamp_ms / 1000
        dt_object = datetime.fromtimestamp(timestamp_s)
        time_between_insertion = datetime.now() - dt_object

        return time_between_insertion.days > 1
