from abc import ABC
from typing import List, Any, Tuple


class Piece(ABC):
    def __init__(self, pos: Tuple[int], color: str, board) -> None:
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.color = color
        self.has_moved = False


    def get_moves(self, board) -> List[Any]:
        squares = []

        for direction in self.get_possible_moves(board):
            for square in direction:
                if square.occupying_piece is not None:
                    if square.occupying_piece.color == self.color:
                        break
                    else:
                        squares.append(square)
                        break

                else:
                    squares.append(square)

        return squares


    def get_valid_moves(self, board) -> List[Any]:
        valid_squares = []
        
        for square in self.get_moves(board):
            if not board.is_in_check(self.color, board_change=[self.pos, square.pos]):
                valid_squares.append(square)
        
        return valid_squares


    def can_move(self, board, square, force=False) -> bool:
        if square in self.get_valid_moves(board) or force:
            return True
        
        return False


    def other_player_move(self, board, selected_pos: Tuple[int], clicked_pos: Tuple[int]) -> bool:
        for highlighted in board.squares:
            highlighted.highlight = False 


    def move(self, board, square, force=False) -> bool:
        print('def move')
        for highlighted in board.squares:
            highlighted.highlight = False 

        if self.can_move(board, square, force):
            prev_square = board.get_square_from_pos(self.pos)
            self.pos, self.x, self.y = square.pos, square.x, square.y
            prev_square.occupying_piece = None
            square.occupying_piece = self
            board.selected_piece = None
            self.has_moved = True
            
            if self.notation == ' ': # Why its not like 'P'
                if self.y == 0 or self.y == 7:
                    from pieces import Queen # wtf
                    square.occupying_piece = Queen(
                        (self.x, self.y), self.color, board 
                    )
            
            if self.notation == 'K':
                if prev_square.x - self.x == 2:
                    rook = board.get_piece_from_pos((0, self.y))
                    rook.move(board, board.get_square_from_pos((3, self.y)), force=True)
                elif prev_square.x - self.x == -2:
                    rook = board.get_piece_from_pos((7, self.y))
                    rook.move(board, board.get_square_from_pos((5, self.y)), force=True)
            
            return True
        
        else:
            print('else again')
            board.selected_piece = None
            return False


    def attacking_squares(self, board) -> List[Any]:
        return self.get_moves(board)
