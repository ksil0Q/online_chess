import json
import logging
from queue import Queue
from typing import Tuple, Dict, Optional, Any, TypeVar
from websocket import create_connection, WebSocket, WebSocketException, WebSocketProtocolException


from .messages import responses, MessageMatcher,\
                        BaseMessage as _BaseMessage, BaseResponse as _BaseResponse


BaseMessage = TypeVar('BaseMessage', bound=_BaseMessage)
BaseResponse = TypeVar('BaseResponse', bound=_BaseResponse)


class WSManager:
    def __init__(self, uri: str, ) -> None:
        self.response_types = self.__get_response_types()
        self.last_messages = MessageMatcher()
        self.uri = uri
        self.ws = self.__create_connection()


    def __create_connection(self) -> Optional[WebSocket]:
        try:
            ws = create_connection(self.uri)
            return ws
        except WebSocketException as e:
            logging.info(e)


    def __get_response_types(self) -> Dict[int, Any]:
        types = {}
        for response in responses:
            types[response.message_type] = response

        return types


    def push_response_to_queue(self, object_queue: Queue, message_id: str) -> None:
        object_queue.put(self.last_messages.get(message_id))


    def send_and_wait(self, message: BaseMessage, pending_queue: Queue) -> None:

        self.send_message(message)
        self._get_messages(self.push_response_to_queue, pending_queue, message.message_id) 


    def send_message(self, message: BaseMessage) -> bool:
        if isinstance(message, _BaseMessage):
            serialized_message = self._serialize(message.to_dict())
        else:
            raise TypeError(f'unsupport type for message: {type(message)}')
        
        try:
            self.ws.send(serialized_message)
            self.last_messages.put_request(message)
            return True
        except WebSocketException as e:
            logging.info(e)
            return False


    def _get_messages(self, on_message=None, *args) -> None:
        got_message = False
        while not got_message:
            try:
                data = self.ws.recv()
                print(f"received data {data}")
                deserialized_data = self._deserialize(data)
                self.last_messages.put_response(deserialized_data)
                got_message = True

                if on_message:
                    on_message(*args)
            except WebSocketProtocolException:
                continue


    def get_message(self, message_id: str) -> Tuple[BaseMessage, BaseResponse]:
        if self.last_messages.empty():
            self._get_messages()

        return self.last_messages.get(message_id)


    def _serialize(self, message: Dict[str, str]) -> str:
        return json.dumps(message)


    def _deserialize(self, message: str) -> BaseResponse:
        message = json.loads(message)
        return self.response_types[message['message_type']].from_dict(message)


    def __del__(self):
        self.ws.close()
