class SingletonMetaClass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        print(cls._instances)
        instance = cls._instances.get(cls)
        if instance is None:
            instance = cls._instances[cls] = super().__call__(*args, **kwargs)
        return instance


class SingletonMixin(metaclass=SingletonMetaClass):
    pass
