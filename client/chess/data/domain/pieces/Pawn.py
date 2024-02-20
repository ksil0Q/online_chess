import pygame
from typing import Tuple, List, Any

from domain.board.Piece import Piece


class Pawn(Piece):
    def __init__(self, pos: Tuple[int], color: str, board) -> None:
        super().__init__(pos, color, board)

        img_path = '/'.join(['data/imgs', f'{color[0]}_pawn.png'])

        img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(img, (board.tile_width - 20, board.tile_height - 20))

        self.notation = ' '


    def get_possible_moves(self, board) -> List[Any]:
        possible_moves = []

        temp_moves = []

        if self.color == 'white':
            one_step = -1
            double_step = -2
        else:
            one_step = 1
            double_step = 2
        
        temp_moves.append((0, one_step))
        if not self.has_moved:
            temp_moves.append((0, double_step))
        

        for move in temp_moves:
            new_pos = (self.x, self.y + move[1])
            if new_pos[1] < 8 and new_pos[1] >= 0:
                possible_moves.append(board.get_square_from_pos(new_pos))
        
        return possible_moves


    def get_moves(self, board) -> List[Any]:
        moves = []

        for square in self.get_possible_moves(board):
            if square.occupying_piece != None:
                break
            else:
                moves.append(square)
        
        if self.color == 'white':
            if self.x + 1 < 8 and self.y - 1 >= 0:
                square = board.get_square_from_pos(
					(self.x + 1, self.y - 1)
				)
                if square.occupying_piece != None:
                    if square.occupying_piece.color != self.color:
                        moves.append(square)
            if self.x - 1 >= 0 and self.y - 1 >= 0:
                square = board.get_square_from_pos(
					(self.x - 1, self.y - 1)
				)
                if square.occupying_piece != None:
                    if square.occupying_piece.color != self.color:
                        moves.append(square)

        elif self.color == 'black':
            if self.x + 1 < 8 and self.y + 1 < 8:
                square = board.get_square_from_pos(
					(self.x + 1, self.y + 1)
				)
                if square.occupying_piece != None:
                    if square.occupying_piece.color != self.color:
                        moves.append(square)
            if self.x - 1 >= 0 and self.y + 1 < 8:
                square = board.get_square_from_pos(
					(self.x - 1, self.y + 1)
				)
                if square.occupying_piece != None:
                    if square.occupying_piece.color != self.color:
                        moves.append(square)

        return moves


    def attacking_squares(self, board) -> List[Any]:
        moves = self.get_moves(board)
        return [i for i in moves if i.x != self.x]
