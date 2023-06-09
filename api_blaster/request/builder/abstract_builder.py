from abc import abstractmethod


class AbstractBuilder:

    @abstractmethod
    def set_url(self):
        pass

    @abstractmethod
    def set_headers(self):
        pass

    @abstractmethod
    def set_name(self):
        pass
