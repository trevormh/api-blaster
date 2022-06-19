from abc import ABC, abstractmethod
from typing import Any, Optional, TYPE_CHECKING, Union, Callable, List


if TYPE_CHECKING:
    from api_blaster.request.http_request import HttpRequest
    from api_blaster.request.formatter.handler import Handler


class AbstractHandler(ABC):
    request_str: str = ''

    @abstractmethod
    def set_next(self, handler: 'Handler') -> 'Handler':
        pass

    @abstractmethod
    def next(self, request: 'HttpRequest', req_list: List[str]) -> List[str]:
        pass
