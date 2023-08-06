# encoding: utf-8


class MyBaseException(Exception):
    def __init__(self, message, status_code=None):
        super(MyBaseException, self).__init__(message)
        self.message = message
        self.status_code = status_code


class JsonnetEvalException(MyBaseException):
    pass


class NamespaceConfigException(MyBaseException):
    pass


class ApplicationConfigException(MyBaseException):
    pass


class ApplicationRelationException(MyBaseException):
    pass


class ApplicationNotFoundException(MyBaseException):
    pass


class ApplicationRelationMismatchException(MyBaseException):
    pass


class InvalidDependenceException(MyBaseException):
    pass


class InvalidApplicationTreeRoot(MyBaseException):
    pass


class KubeException(MyBaseException):
    def __init__(self, message, status_code=None):
        super(KubeException, self).__init__(message, status_code)


class ObjectDoesNotExist(MyBaseException):
    def __init__(self, message, status_code=None):
        super(ObjectDoesNotExist, self).__init__(message, status_code)
