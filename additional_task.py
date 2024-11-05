import time
from functools import wraps


def retry(times=3, delay=1, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt < times - 1:
                        print(
                            f"attempt {attempt + 1} of {times + 1} failed: {e}")
                        time.sleep(delay)

        return wrapper

    return decorator


@retry(times=5, delay=2, exceptions=(ValueError, KeyError))
def test_function(x):
    if x == 0:
        raise ValueError("Zero value")
    return 1 / x


test_function(0)
