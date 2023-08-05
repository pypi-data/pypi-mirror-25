class AppException(RuntimeError):

    def __init__(self, *args, **kwargs):
        self.err_code = 1000
        RuntimeError.__init__(self, *args, **kwargs)

    def __str__(self):
        return self.__class__.__name__ + "[" + str(self.err_code) + "] " + RuntimeError.__str__(self)


class NotFoundException(AppException):
    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1001


class IllegalArgumentException(AppException):
    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1002


class DuplicatedException(AppException):
    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1003


class IllegalOperationException(AppException):
    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1004


class FailedToLoadException(AppException):
    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1005


class CannotConnectException(AppException):
    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1006


class StateErrorException(AppException):
    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1007


class InternalErrorException(AppException):
    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1008


class OperationFailedException(AppException):
    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1009


class DatabaseErrorException(AppException):
    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1010


class InvalidTypeException(AppException):
    def __init__(self, *args, **kwargs):
        AppException.__init__(self, *args, **kwargs)
        self.err_code = 1011
