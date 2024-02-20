from typing import Dict, Any, Tuple, Type


from .BaseMessage import BaseMessage, BaseResponse


class PlayersMove(BaseMessage):
    message_type = 4
    def __init__(self, session_id: str, user_id: int, selected_piece_pos: Tuple[int], clicked_piece_pos: Tuple[int]) -> None:
        super().__init__(session_id, user_id)
        self.selected_piece_pos = selected_piece_pos
        self.clicked_piece_pos = clicked_piece_pos


    def to_dict(self) -> Dict[str, Any]:
        request_message = {'message_type': self.message_type, 'message_id': self.message_id}
        
        payload = {'session_id': self.session_id, 'user_id': self.user_id,
                   'selected_piece_pos': self.selected_piece_pos, 'clicked_piece_pos': self.clicked_piece_pos}
        
        request_message['payload'] = payload

        return request_message


class PlayersMoveResponse(BaseResponse):
    message_type = 4
    def __init__(self, session_id: str, user_id: int,
                message_id: str, selected_piece_pos: Tuple[int],
                clicked_piece_pos: Tuple[int]) -> None:
        
        super().__init__(session_id, user_id, message_id)
        self.selected_piece_pos = selected_piece_pos
        self.clicked_piece_pos = clicked_piece_pos


    @classmethod
    def from_dict(cls, message: Dict[str, Any]) -> Type['PlayersMove']:
        if message['message_type'] != cls.message_type:
            raise ValueError('incorrect message type')
        
        payload = message['payload']
        return PlayersMoveResponse(payload['session_id'], payload['user_id'], 
                           message['message_id'], payload['selected_piece_pos'],
                           payload['clicked_piece_pos'])
