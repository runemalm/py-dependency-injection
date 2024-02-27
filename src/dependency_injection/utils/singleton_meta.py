class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        instance_key = (cls, *args, frozenset(kwargs.items()))

        if instance_key not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[instance_key] = instance
        return cls._instances[instance_key]
