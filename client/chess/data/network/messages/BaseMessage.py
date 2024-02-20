import random, string
from hashlib import sha256
from typing import Dict, Any
from abc import ABC, abstractmethod

try:
    from data.loader import MESSAGE_ID_SIZE
except ImportError:
    MESSAGE_ID_SIZE = 32


class BaseMessage(ABC):
    message_type = 0
    def __init__(self, session_id: str, user_id: int) -> None:
        self.session_id = session_id
        self.user_id = user_id
        self.message_id = self.__create_id()


    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        pass


    def __create_id(self) -> str:
        return sha256(
            ''.join(random.choices(string.ascii_uppercase + string.digits, k = MESSAGE_ID_SIZE)).encode())\
            .hexdigest()


class BaseResponse(ABC):
    message_type = 0
    def __init__(self, session_id: str, user_id: int, message_id: str) -> None:
        self.session_id = session_id
        self.user_id = user_id
        self.message_id = message_id


    @abstractmethod
    def from_dict(self) -> Dict[str, Any]:
        pass
