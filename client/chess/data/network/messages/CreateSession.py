from typing import Dict, Any, Type


from .BaseMessage import BaseMessage, BaseResponse


class CreateSession(BaseMessage):
    message_type = 2
    def __init__(self, session_id: str, user_id: int) -> None:
        super().__init__(session_id, user_id)


    def to_dict(self) -> Dict[str, Any]:
        request_message = {'message_type': self.message_type, 'message_id': self.message_id}
        
        payload = {'session_id': self.session_id, 'user_id': self.user_id}
        
        request_message['payload'] = payload

        return request_message



class CreateSessionResponse(BaseResponse):
    message_type = 2
    def __init__(self, session_id: str, 
                message_id: str, user_id: int,
                success: bool) -> None:
        
        super().__init__(session_id, user_id, message_id)
        self.success = success

    
    @classmethod
    def from_dict(cls, message: Dict[str, Any]) -> Type['CreateSessionResponse']:
        if message['message_type'] != cls.message_type:
            raise ValueError('incorrect message type')
        
        payload = message['payload']

        return CreateSessionResponse(payload['session_id'], message['message_id'],
                                     payload['user_id'], payload['success'])

