import pygame
from typing import List, Any, Tuple

from domain.board.Piece import Piece


class Rook(Piece):
    def __init__(self, pos: Tuple[int], color: str, board) -> None:
        super().__init__(pos, color, board)

        img_path = '/'.join(['data/imgs/', f'{color[0]}_rook.png'])
        img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(img, (board.tile_width - 20, board.tile_height - 20))

        self.notation = 'R'


    def get_possible_moves(self, board) -> List[Any]:
        possible_moves = []

        moves_north = []
        for y in range(self.y)[::-1]:
            moves_north.append(board.get_square_from_pos((self.x, y)))
        
        possible_moves.append(moves_north)


        moves_east = []
        for x in range(self.x + 1, 8):
            moves_east.append(board.get_square_from_pos((x, self.y)))
        
        possible_moves.append(moves_east)


        moves_south = []
        for y in range(self.y + 1, 8):
            moves_south.append(board.get_square_from_pos((self.x, y)))
        
        possible_moves.append(moves_south)


        moves_west = []
        for x in range(self.x)[::-1]:
            moves_west.append(board.get_square_from_pos((x , self.y)))
            
        possible_moves.append(moves_west)

        return possible_moves
