from .BaseMessage import BaseMessage, BaseResponse
from .VoluntarySurrender import VoluntarySurrender, VoluntarySurrenderResponse
from .PlayersMove import PlayersMove, PlayersMoveResponse
from .CreateSession import CreateSession, CreateSessionResponse
from .GetInfo import GetInfo
from .Authorize import Authorize, AuthorizeResponse
from .GameStart import GameStart, GameStartResponse

from .MessageMatcher import MessageMatcher

requests = [VoluntarySurrender, PlayersMove, CreateSession, GetInfo, Authorize, GameStart]
responses = [AuthorizeResponse, CreateSessionResponse, GameStartResponse, PlayersMoveResponse, VoluntarySurrenderResponse]