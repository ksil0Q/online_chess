from typing import Tuple, List, Dict, Union, Any, TypeVar
from queue import Empty


from .BaseMessage import BaseMessage as _BaseMessage, BaseResponse as _BaseResponse


BaseMessage = TypeVar('BaseMessage', bound=_BaseMessage)
BaseResponse = TypeVar('BaseResponse', bound=_BaseResponse)


class MessageMatcher:
    """Composes pairs of requests and responses, 
    the unmapped ones will be saved in unmatched_requests, 
    saves its as List[Tuple[BaseMessage, BaseResponse]]
    implements the *put, get and empty methods as a queue, historically

    * put_request, put_response
    """

    def __init__(self,
                 base_messages: Tuple[BaseMessage] = None,
                 base_responses: Tuple[BaseResponse] = None) -> None:
        
        self.unmatched_requests = {}
        self.message_pairs = self.__create_message_pairs(base_messages, base_responses)


    def __create_message_pairs(self,
                                  base_messages: Tuple[BaseMessage],
                                  base_responses: Tuple[BaseMessage]) -> Dict[str, Tuple[BaseMessage, BaseResponse]]:

        if not base_messages:
             return {}

        messages_d = dict(map(lambda x: (x.message_id, x), base_messages))
        print(messages_d)
        responses_d = dict(map(lambda x: (x.message_id, x), base_responses))
        print(responses_d)
        message_pairs = {}

        message_id_intersection = set((x.message_id for x in base_messages))\
                                .intersection(set((x.message_id for x in base_responses)))

        for message_id in message_id_intersection:
                message_pairs.update({message_id: (messages_d[message_id], responses_d[message_id])})
                messages_d.pop(message_id)

        if messages_d:
            self.unmatched_requests = messages_d
        
        return message_pairs


    def get(self, request_id: str) -> Tuple[BaseMessage, BaseResponse]:
        message_pair = self.message_pairs.pop(request_id, None)

        if not message_pair:
            message = self.unmatched_requests.get(request_id, None)
            if not message:
                raise Empty(f"{self} has no messages with message_id={request_id}")
            return message, None

        return message_pair


    def put_request(self, request: Union[Dict[str, Any], BaseMessage]) -> None:
        if isinstance(request, _BaseMessage):
            self.unmatched_requests[request.message_id] = request
        elif isinstance(request, Dict):
            self.unmatched_requests[request['message_id']] = request
        else:
            raise TypeError(f'unsupport type for request: {type(request)}')


    def put_response(self, response: BaseResponse) -> None:
        if not isinstance(response, _BaseResponse):
            raise TypeError(f'unsupport type for request: {type(response)}')
        print(response.__dict__)
        request = self.unmatched_requests.pop(response.message_id)
        self.message_pairs[request.message_id] = (request, response)


    def empty(self) -> bool:
        "Return True if MessageMatcher has no message pairs"
        if not self.message_pairs:
            return True
        
        return False