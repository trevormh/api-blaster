from abc import ABC, abstractmethod
from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from handler import Handler


class AbstractHandler(ABC):

    request_str = ''

    @abstractmethod
    def set_next(self, handler: 'Handler') -> 'Handler':
        pass

    @abstractmethod
    def next(self, request, request_str) -> Optional[str]:
        pass
