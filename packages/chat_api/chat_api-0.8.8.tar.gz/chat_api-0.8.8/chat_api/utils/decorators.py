
class ClassProperty(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, cls):
        ret = self.func(instance)
        return ret
