"""
Tools for working with functions and callable objects.

"""
import StringIO
import traceback


class cached_property(object):
    """
    Decorator that converts a method with a single self argument into a
    property cached on the instance.

    Optional ``name`` argument allows you to make cached properties of other
    methods. (e.g.  url = cached_property(get_absolute_url, name='url') )
    """
    def __init__(self, func, name=None):
        self.func = func
        self.__doc__ = getattr(func, '__doc__')
        self.name = name or func.__name__

    def __get__(self, instance, cls=None):
        if instance is None:
            return self
        res = instance.__dict__[self.name] = self.func(instance)
        return res


def get_traceback():
    except_trace = StringIO.StringIO()
    traceback.print_exc(file=except_trace)
    except_content = str(except_trace.getvalue())
    except_trace.close()
    return except_content
