import abc


class AbstractModule(object):
    name = "abstract"
    value = None

    @abc.abstractmethod
    def __init__(self, app):
        self.value = None
