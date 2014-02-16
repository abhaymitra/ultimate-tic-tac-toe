from functools import wraps
import errno
import os
import signal
import time



class TimeoutError(Exception):
    pass

def timeout(seconds, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            alarmtime = int(seconds[0])-int(seconds[1])
            if alarmtime <0 :
                raise TimeoutError      
            try:
                t = time.time()
                result = func(*args, **kwargs)
                seconds[1] = seconds[1] + (time.time() - t)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

def timer(l):
    def decorator(func):
        def wrapper(*args,**kwargs):
            t = time.time()
            result = func(*args, **kwargs)
            l[0] = l[0] + (time.time() - t)
            return result

        return wraps(func)(wrapper)

    return decorator



