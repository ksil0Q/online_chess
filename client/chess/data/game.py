import pygame
import logging
import random, string
from queue import Queue
from threading import Thread
from typing import Tuple, Optional, Dict, Any, TypeVar


from domain import Board
from loader import WEBSOCKET_URI, WINDOW_SIZE, SESSION_ID_SIZE
from network import WSManager, VoluntarySurrender, PlayersMove, Authorize, CreateSession, GameStart,\
                    BaseMessage as _BaseMessage, BaseResponse as _BaseResponse


BaseMessage = TypeVar('BaseMessage', bound=_BaseMessage)
BaseResponse = TypeVar('BaseResponse', bound=_BaseResponse)


class Game:
    """class that will play for the second player,
        decides whose turn to its walk"""

    def __init__(self) -> None:
        self.turn = 0
        self.playing_color = 'black' if not self.turn else 'white'
        self.ws = WSManager(WEBSOCKET_URI)
        self.input_data = Queue()
        self.output_data = Queue()
        self.session_id = -1
        self.user_id = -1
        self.user_score = None
        pygame.init()
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1], 'white') # TODO colors as int


    def _send_data(self, message: BaseMessage = None) -> Optional[Thread]:
        """waits for a response"""
        if not message:
            if not self.output_data.empty():
                message = self.output_data.get()
            else:
                return
        
        if not isinstance(message, _BaseMessage):
            raise TypeError(f'unsupport type for message: {type(message)}')
        print(message.__dict__)
        expectant = Thread(target=self.ws.send_and_wait, args=(message, self.input_data))
        expectant.daemon = True # its not necessary to wait other player, user can give up or do other stuff
        expectant.start()
        # expectant.join() main thread dont need to wait 'expectant' thread terminate
        return expectant


    def _get_data(self, message_id: str) -> Dict[str, str]:
        self.new_data = self.ws.get_message(message_id)


    def startup(self):
        pass


    def authorize(self, login: str, password: str) -> bool:
        request = Authorize(self.session_id, self.user_id, login, password)
        if not self.ws.send_message(request):
            return False
        
        _, response = self.ws.get_message(request.message_id)
        if not response.auth:
            return False
        
        self.user_score = response.user_score
        self.user_id = response.user_id

        return True

    
    def create_session(self) -> bool:
        session_id = self.__create_session_id()
        request = CreateSession(session_id, self.user_id)

        if not self.ws.send_message(request):
            return False

        _, response = self.ws.get_message(request.message_id)

        if not response.success:
            return False

        self.session_id = session_id
        return True


    def ready_to_start_game(self) -> bool:
        request = GameStart(self.session_id, self.user_id)
        if not self.ws.send_message(request):
            return False

        _, response = self.ws.get_message(request.message_id)

        self.turn = response.turn
        self.playing_color = 'white' if self.turn else 'black'

        return True


    def _draw(self, display: pygame.Surface):
        display.fill('white')
        self.board.draw(display)
        pygame.display.update()


    def __create_session_id(self) -> str:
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k = SESSION_ID_SIZE))


    def apply_another_players_action(self, message_pair: Tuple[BaseMessage, BaseResponse]) -> None:
        _, response = message_pair
        if response.message_type == PlayersMove.message_type:

            self.board.change_selected_piece(response.selected_piece_pos)
            clicked_square = self.board.get_square_from_pos(response.clicked_piece_pos)
            self.board.selected_piece.move(self.board, clicked_square)
            self.board.selected_piece = None
            self.turn = 1
        elif response.message_type == VoluntarySurrender.message_type:
            pass


    def play(self) -> None:
        running = True
        while running:
            if not self.input_data.empty():
                data = self.input_data.get()
                self.apply_another_players_action(data)
                self._draw(self.screen)
        
            mx, my = pygame.mouse.get_pos()
            for event in pygame.event.get():
                # Quit the game if the user presses the close button
                if event.type == pygame.QUIT:
                    running = False
                    self._send_data(VoluntarySurrender(2, 123))
                elif event.type == pygame.MOUSEBUTTONDOWN: 
                    # If the mouse is clicked
                    print(f'mouse clicked {event.button}')
                    if event.button == 1:
                        if self.handle_click(mx, my):
                            self._send_data()
                            
                    elif event.button == 3:
                        self.board.cancel_click()

            if self.board.is_in_checkmate('black'): # If black is in checkmate
                print('White wins!')
                running = False
            elif self.board.is_in_checkmate('white'): # If white is in checkmate
                print('Black wins!')
                running = False
            # Draw the board)
            self._draw(self.screen)


    def handle_click(self, mx: int, my: int) -> bool:
        # returns True if piece was moved
        x = mx // self.board.tile_width
        y = my // self.board.tile_height

        clicked_square = self.board.get_square_from_pos((x, y))

        if self.board.selected_piece is None:
            if clicked_square.occupying_piece is not None:
                if clicked_square.occupying_piece.color == self.playing_color:
                    print('first if')
                    self.board.selected_piece = clicked_square.occupying_piece
        
        elif self.board.selected_piece.can_move(self.board, clicked_square) and self.turn:
            # saving selected_piece.pos because 'move' function change its values 
            selected_piece_pos = self.board.selected_piece.pos
            self.board.selected_piece.move(self.board, clicked_square)

            self.turn = 0
            self.output_data.put(PlayersMove(12, 21, selected_piece_pos, clicked_square.pos))
            return True
        
        elif clicked_square.occupying_piece is not None:
            if clicked_square.occupying_piece.color == self.playing_color:
                print('elif 2')
                self.board.selected_piece = clicked_square.occupying_piece
        
        return False
