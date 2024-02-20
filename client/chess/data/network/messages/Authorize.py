from typing import Dict, Any, Type


from .BaseMessage import BaseMessage, BaseResponse


class Authorize(BaseMessage):
    message_type = 1
    def __init__(self, session_id: str, user_id: int, login: str, password: str) -> None:
        super().__init__(session_id, user_id)
        self.login = login
        self.password = password


    def to_dict(self) -> Dict[str, Any]:
        request_message = {'message_type': self.message_type, 'message_id': self.message_id}
        
        payload = {'session_id': self.session_id, 'user_id': self.user_id,
                   'login': self.login, 'password': self.password}
        
        request_message['payload'] = payload

        return request_message


class AuthorizeResponse(BaseResponse):
    message_type = 1
    def __init__(self, session_id: str, user_id: int,
                message_id: str, auth: bool, user_score: int) -> None:
        
        super().__init__(session_id, user_id, message_id)
        self.auth = auth
        self.user_score = user_score


    @classmethod
    def from_dict(cls, message: Dict[str, Any]) -> Type['AuthorizeResponse']:
        if message['message_type'] != cls.message_type:
            raise ValueError('incorrect message type')
        
        payload = message['payload']
        print
        return AuthorizeResponse(payload['session_id'], payload['user_id'],
                                 message['message_id'],
                                 payload['auth'], payload['user_score'])
