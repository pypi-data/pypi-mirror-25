import time
from functools import wraps

from loader.function import load


class ContextDecorator(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __enter__(self):
        self.start_time = time.time()
        # Note: Returning self means that in "with ... as x", x will be self
        return self

    def __exit__(self, typ, val, traceback):
        self.end_time = time.time()
        return self

    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kw):
            with self:
                return f(*args, **kw)
        return wrapper


class ShowTime(ContextDecorator):
    def __exit__(self, typ, val, traceback):
        super(ShowTime, self).__exit__(typ, val, traceback)
        print("elapsed: {}".format(self.end_time - self.start_time))


class RedirectException(ContextDecorator):
    def __call__(self, f):
        @wraps(f)
        def wrapper(*args, **kw):
            with self:
                on_error = self.__dict__.get('on_error')
                if on_error:
                    try:
                        ret = f(*args, **kw)
                        return ret
                    except Exception as e:
                        kw.update({'error': e})
                        error_handler = load(on_error) if isinstance(on_error, str) else on_error
                        return error_handler(*args, **kw)
                else:
                    return f(*args, **kw)
        return wrapper


class SingleDict2List(ContextDecorator):
    def __call__(self, f):
        @wraps(f)
        def wrapper(one):
            with self:
                ones = [one] if not isinstance(one, list) else one
                return f(ones)
        return wrapper
