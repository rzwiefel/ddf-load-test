import os
import re
import time

true_regex = re.compile(r'^t(rue)?$', re.I)


def timeit(func):
    def decorator(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        delta = time.time() - start
        if delta > 0.1:
            print("Func '%s' took %s" % (func.__name__, delta))
        return result

    return decorator


def switchable(variable_name, execute_if=True, default_return=None):
    assert isinstance(variable_name, str), 'Variable name must be a string of variable name to check'

    def wrapper(func):
        def decorated(*args, **kwargs):
            if execute_if == (true_regex.fullmatch(os.getenv(variable_name, 'false')) is not None):
                return func(*args, **kwargs)
            else:
                return default_return

        return decorated

    return wrapper
