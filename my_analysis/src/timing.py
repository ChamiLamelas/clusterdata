from datetime import timedelta, datetime
from math import ceil
import sys
import time


def nice_seconds_string(seconds):
    return str(timedelta(seconds=ceil(seconds)))


class MyTimerException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class MyTimer:
    def __init__(self, stream=sys.stdout):
        self.stream = stream
        self.start_time = None
        self.stop_time = None
        self.task = None

    def start(self, task=None):
        self.task = ((task + ' ') if task is not None else '')
        print(
            f"{self.task}start time: {datetime.now().strftime('%m/%d/%Y %I:%M:%S %p')}", file=self.stream)
        self.start_time = time.time()

    def stop(self):
        self.stop_time = time.time()
        if self.start_time is None:
            raise MyTimerException(f"stop( ) called without calling start( )")
        print(f"{self.task}runtime (h:mm:ss): {nice_seconds_string(time.time() - self.start_time)}", file=self.stream)
        self.start_time = None
