import pygame
from typing import Tuple, List, Any


from domain.board.Piece import Piece


class Knight(Piece):
    def __init__(self, pos: Tuple[int], color: str, board) -> None:
        super().__init__(pos, color, board)

        img_path = '/'.join(['data/imgs', f'{color[0]}_knight.png'])

        img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(img, (board.tile_width - 20, board.tile_height - 20))

        self.notation = 'N'


    def get_possible_moves(self, board) -> List[Any]:
        possible_moves = []

        knight_moves = [
            (1, -2),
            (2, -1),
			(2, 1),
			(1, 2),
			(-1, 2),
			(-2, 1),
			(-2, -1),
			(-1, -2)
        ]

        for move in knight_moves:
            new_pos = (self.x + move[0], self.y + move[1])
            if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                possible_moves.append([board.get_square_from_pos(new_pos)])

            return possible_moves
