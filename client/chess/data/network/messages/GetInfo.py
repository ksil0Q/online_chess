from typing import Dict, Any


from .BaseMessage import BaseMessage


class GetInfo(BaseMessage):
    message_type = -1 # class reserved for future extension
    def __init__(self, session_id: str, user_id: int) -> None:
        super().__init__(session_id, user_id)


    def to_dict(self) -> Dict[str, Any]:
        request_message = {'message_type': self.message_type, 'message_id': self.message_id}
        
        payload = {'session_id': self.session_id, 'user_id': self.user_id,
                   'message_id': self.message_id,}
        
        request_message['payload'] = payload

        return request_message
