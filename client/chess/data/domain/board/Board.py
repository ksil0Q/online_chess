import pygame
from typing import List, Any, Tuple

from .Piece import Piece
from .Square import Square
from domain.pieces import Rook, Bishop, Knight, Queen, King, Pawn


class Board:
    def __init__(self, width: int, height: int, turn: str) -> None:
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_piece: Piece = None

        self.config = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['wP','wP','wP','wP','wP','wP','wP','wP'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR'],
        ]

        self.squares = self.generate_squares()
        self.setup_board()


    def generate_squares(self) -> List[Square]:
        squares = []

        for y in range(8):
            for x in range(8):
                squares.append(Square(x, y, self.tile_width, self.tile_height))
        
        return squares


    def get_square_from_pos(self, pos: Tuple[int]) -> Square:
        for square in self.squares:
            if (square.x, square.y) == (pos[0], pos[1]):
                return square


    def get_piece_from_pos(self, pos: Tuple[int]) -> Piece:
        return self.get_square_from_pos(pos).occupying_piece


    def change_selected_piece(self, pos: Tuple[int]) -> Piece:
        new_selected_piece = self.get_piece_from_pos(pos)
        self.selected_piece = new_selected_piece

        return new_selected_piece


    def setup_board(self) -> None:
        for y, row in enumerate(self.config):
            for x, piece in enumerate(row):
                if piece != '':
                    square = self.get_square_from_pos((x, y))

                    if piece[1] == 'R':
                        square.occupying_piece = Rook(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    
                    elif piece[1] == 'N':
                        square.occupying_piece = Knight(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    
                    elif piece[1] == 'B':
                        square.occupying_piece = Bishop(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    
                    elif piece[1] == 'Q':
                        square.occupying_piece = Queen(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    
                    elif piece[1] == 'K':
                        square.occupying_piece = King(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )
                    
                    elif piece[1] == 'P':
                        square.occupying_piece = Pawn(
                            (x, y), 'white' if piece[0] == 'w' else 'black', self
                        )


    def is_in_check(self, color: str, board_change: List[Tuple[int]] = None) -> bool:
        res = False
        king_pos = None

        changing_piece = None
        old_square = None
        new_square = None
        new_square_old_piece = None

        if board_change is not None:
            for square in self.squares:
                if square.pos == board_change[0]:
                    changing_piece = square.occupying_piece
                    old_square = square
                    old_square.occupying_piece = None
            
            for square in self.squares:
                if square.pos == board_change[1]:
                    new_square = square
                    new_square_old_piece = new_square.occupying_piece
                    new_square.occupying_piece = changing_piece
        
        pieces = [i.occupying_piece for i in self.squares if i.occupying_piece is not None]

        if changing_piece is not None:
            if changing_piece.notation == 'K':
                king_pos = new_square.pos
        
        if king_pos == None:
            for piece in pieces:
                if piece.notation == 'K' and piece.color == color:
                    king_pos = piece.pos
            
        for piece in pieces:
            if piece.color != color:
                for square in piece.attacking_squares(self):
                    if square.pos == king_pos:
                        res = True
        
        if board_change is not None:
            old_square.occupying_piece = changing_piece
            new_square.occupying_piece = new_square_old_piece
        
        return res


    def is_in_checkmate(self, color: str) -> bool:
        res = False

        for piece in [i.occupying_piece for i in self.squares]:
            if piece != None:
                if piece.notation == 'K' and piece.color == color:
                    king = piece
        
        if king.get_valid_moves(self) == []:
            if self.is_in_check(color):
                res = True
            
        return res


    def draw(self, display) -> None:
        if self.selected_piece is not None:
            self.get_square_from_pos(self.selected_piece.pos).highlight = True
            for square in self.selected_piece.get_valid_moves(self):
                square.highlight = True
        
        for square in self.squares:
            square.draw(display)


    def cancel_click(self) -> None:
        self.selected_piece = None
        for square in self.squares:
            square.highlight = False
