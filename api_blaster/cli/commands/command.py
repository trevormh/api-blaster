from abc import abstractmethod


class Command:

    @abstractmethod
    def execute(self):
        pass
