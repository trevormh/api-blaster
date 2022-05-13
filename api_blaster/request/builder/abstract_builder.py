from abc import abstractmethod


class AbstractBuilder:

    @abstractmethod
    def set_url(self):
        pass

    @abstractmethod
    def set_method(self):
        pass

    @abstractmethod
    def set_name(self):
        pass

    # @abstractmethod
    # def execute(self):
    #     pass

