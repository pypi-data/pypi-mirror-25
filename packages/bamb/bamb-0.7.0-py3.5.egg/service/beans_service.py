import domain.exceptions
import types


class BeanFactory(object):

    def __init__(self, app=None, *args, **kwargs):
        self.__app = app
        self.__beans = {}
        m = __import__("persist.beans", fromlist=("persist"))
        d = getattr(m, "beans")
        self.__beans.update(d)
        m = __import__("service.beans", fromlist=("service"))
        d = getattr(m, "beans")
        self.__beans.update(d)
        m = __import__("rest.beans", fromlist=("rest"))
        d = getattr(m, "beans")
        self.__beans.update(d)

    def start(self, *args, **kwargs):
        for k, v in self.__beans.items():
            my_kwargs = {}
            init_method = v.__init__
            if isinstance(init_method, types.FunctionType):
                vn = init_method.__code__.co_varnames
                if "app" in vn:
                    my_kwargs["app"] = self.__app

            self.__beans[k] = v(**my_kwargs)

    def get_bean(self, key, singleton=True, silence=False):
        bean = self.__beans.get(key, None)
        if bean is None:
            if not silence:
                raise domain.exceptions.NotFoundException("bean not found : " + str(key))
        if singleton:
            return bean
        else:
            return bean.__class__()
