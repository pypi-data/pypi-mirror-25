from abc import abstractmethod

__all__ = ["AbstractScript", "AbstractCollector"]


class AbstractScript(object):
    def __init__(self, manager):
        self.manager = manager

    @abstractmethod
    async def main(self):
        pass


class AbstractCollector(object):
    @abstractmethod
    def load_from_module(self, module):
        pass
