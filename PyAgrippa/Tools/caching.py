from functools import wraps


def cachedMethod(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        self: object = args[0]
        funcName = func.__name__
        inputs = tuple(list([args[1:]]) + list(kwargs.values()))
        if not hasattr(self, '__cached__'):
            self.__cached__ = {}
        if funcName not in self.__cached__:
            self.__cached__[funcName] = {}
        if inputs not in self.__cached__[funcName]:
            returnVal = func(*args, **kwargs)
            self.__cached__[funcName][inputs] = returnVal
        return self.__cached__[funcName][inputs]
    return wrapper
