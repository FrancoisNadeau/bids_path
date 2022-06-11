
from time import time


class TimeCheck:
    """
    Python decorator to view execution time of a program.

    Implementation:
        @TimeCheck
        def some_function(delay):
            return some_function(*args, **kwargs)
    """
    def __init__(self, func):
        self.function = func

    def __call__(self, *args, **kwargs):
        start_time = time()
        result = self.function(*args, **kwargs)
        end_time = time()
        print("Execution took {} seconds".format(end_time - start_time))
        return result
