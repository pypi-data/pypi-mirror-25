def singleton(cls):
    """
    Singleton decorator
    """
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return get_instance
