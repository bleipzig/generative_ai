import logging
import logging.config
import time
from functools import wraps
from pprint import pprint


def frame(func):
    wraps(func)
    def wrapper(*args, **kwargs):
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(asctime)s [%(name)s]: %(message)s', datefmt='%b %d %H:%M:%S')
        logger = logging.getLogger(func.__name__)
        print(" START ".center(120, '-'))
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        logging.debug(f"Finished executing {func.__name__} in {end - start:.6f} seconds")
        print(" END ".center(120, '-'))
        return result
    return wrapper

def timeit_log(logger):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            end = time.perf_counter()
            logger.info(f"Finished executing {func.__name__} in {end - start:.6f} seconds")
            return result
        return wrapper
    return decorator

def show_func_return_value(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print("Returned Value:")
        pprint(result)
        print("Data Type:", type(result).__name__)
        return result
    return wrapper