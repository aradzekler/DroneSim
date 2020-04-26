import time
import warnings


def get_current_time():
    try:
        # get monotonic time to ensure that time deltas are always positive
        _current_time = time.monotonic  # monotonic clock is a clock that cannot go backwards.
    except AttributeError:
        # time.monotonic() not available (using python < 3.3), fallback to time.time()
        _current_time = time.time
        warnings.warn('time.monotonic() is not available in Python version < 3.3, using time.time() instead.')


'''
Clamping method, clamping shuts down our integral to stop it from working when we dont need it
to work, like in a case of a drone trying to lift off but we are holding it, integral value
will rise and when we will let go, the drone will jump up and overshoot because integral term is too high,
this is called Integral Windup). 
'''


def clamp(value, limits):
    lower, upper = limits
    if value is None:
        return None
    elif upper is not None and value > upper:
        return upper
    elif lower is not None and value < lower:
        return lower
    return value
