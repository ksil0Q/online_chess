import pygame
from typing import Tuple, List, Any

from domain.board.Piece import Piece


class Bishop(Piece):
    def __init__(self, pos: Tuple[int], color: str, board) -> None:
        super().__init__(pos, color, board)

        img_path = '/'.join(['data/imgs', f'{color[0]}_bishop.png'])

        img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(img, (board.tile_width - 20, board.tile_height - 20))

        self.notation = 'B'


    def get_possible_moves(self, board) -> List[Any]:
        possible_moves = []

        moves_ne = []
        for i in range(1, 8):
            if self.x + i > 7 or self.y - i < 0:
                break

            moves_ne.append(board.get_square_from_pos((self.x + i, self.y - i)))
        
        possible_moves.append(moves_ne)


        moves_se = []
        for i in range(1, 8):
            if self.x + i > 7 or self.y + i > 7:
                break
            moves_se.append(board.get_square_from_pos((self.x + i, self.y + i)))

        possible_moves.append(moves_se)


        moves_sw = []
        for i in range(1, 8):
            if self.x - i < 0 or self.y + i > 7:
                break
            moves_sw.append(board.get_square_from_pos((self.x - i, self.y + i)))

        possible_moves.append(moves_sw)


        moves_nw = []
        for i in range(1, 8):
            if self.x - i < 0 or self.y - i < 0:
                break
            moves_nw.append(board.get_square_from_pos((self.x - i, self.y - i)))

        possible_moves.append(moves_nw)

        return possible_moves
