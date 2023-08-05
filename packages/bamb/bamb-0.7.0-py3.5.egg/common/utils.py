class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False

    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration

    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False

from functools import wraps

PRIMARY_TYPES = [int, float, bool, str, list, tuple, dict]
PRIMARY_SIMPLE_TYPES = [int, float, bool, str]



def flatten(*args, max_depth=32, current_depth=0):
    e = []
    d = current_depth
    r = False
    for v in args:
        if type(v) in [list, tuple, set]:
            r = True
            d = current_depth + 1
            if current_depth < max_depth:
                if isinstance(v, list):
                    e.extend(v)
                else:
                    e.extend(list(v))
            else:
                e.append(v)
        else:
            e.append(v)
    if r and (d < max_depth):
        return flatten(*e, max_depth=max_depth, current_depth=d)
    else:
        return e


def is_instance_of(obj, types=PRIMARY_TYPES, recursive=False, assignable=True):
    t = type(obj)
    ts = flatten(types)
    if recursive:
        tp = ()
        if t in [list, tuple, set]:
            tp = tuple(obj)
        if t == dict:
            tp = tuple(obj.values)
        if len(tp) > 0:
            for v in tp:
                if not is_instance_of(v, ts, True, assignable):
                    return False
            return True
        else:
            if assignable:
                for ts1 in ts:
                    if isinstance(obj, ts1):
                        return True
                return False
            else:
                return t in ts
    else:
        if assignable:
            for ts1 in ts:
                if isinstance(obj, ts1):
                    return True
            return False
        else:
            return t in ts


class LockContext(object):
    def __init__(self, lock):
        self.lock = lock

    def __enter__(self):
        return self.lock

    def __exit__(self, exception_type, value, traceback):
        return exception_type is None


def create_instance(full_name, *args, **kwargs):
    if not isinstance(full_name, str):
        raise RuntimeError("can not create instance for empty name!")
    names = full_name.split(".")
    if len(names) < 2:
        raise RuntimeError("invalid name : " + full_name)
    class_name = names[-1]
    module_name = names[-2]
    if len(names) > 2:
        froms = names[0 : len(names) - 2]
    else:
        froms = []
    try:
        if len(froms) > 0:
            module = __import__(froms[0])
            if len(froms) > 1:
                for sm in froms[1:]:
                    module = getattr(module, sm)
            module = getattr(module, module_name)

        else:
            module = __import__(module_name)
        class_ = getattr(module, class_name)
        inst = class_(*args, **kwargs)
        return inst
    except Exception as err:
        raise RuntimeError("failed to load class froms = " + str(froms) + ", module = " +
                           module_name + ", class = " + class_name + ". exception is " + str(err))
