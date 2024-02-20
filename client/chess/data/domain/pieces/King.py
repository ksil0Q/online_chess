import pygame
from typing import Tuple, List, Any, Optional


from domain.board.Piece import Piece


class King(Piece):
    QUEENSIDE = 'queenside'
    KINGSIDE = 'kingside'

    def __init__(self, pos: Tuple[int], color: str, board) -> None:
        super().__init__(pos, color, board)

        img_path = '/'.join(['data/imgs/', f'{color[0]}_king.png'])
        img = pygame.image.load(img_path)
        self.img = pygame.transform.scale(img, (board.tile_width - 20, board.tile_height - 20))
        
        self.notation = 'K'


    def get_possible_moves(self, board) -> List[Any]:
        possible_moves = []
        king_moves = [
            (0, -1), # north
			(1, -1), # ne
			(1, 0), # east
			(1, 1), # se
			(0, 1), # south
			(-1, 1), # sw
			(-1, 0), # west
			(-1, -1), # nw
        ]

        for move in king_moves:
            new_pos = (self.x + move[0], self.y + move[1])

            if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                possible_moves.append([board.get_square_from_pos(new_pos)])
        
        return possible_moves


    def can_castle(self, board) -> Optional[str]:
        if not self.has_moved:

            if self.color == 'white':
                y = 7
            else:
                y = 0

            queenside_rook = board.get_piece_from_pos((0, y))

            if queenside_rook != None:
                if not queenside_rook.has_moved:
                    pieces = [board.get_piece_from_pos((i, 7)) for i in range(1, 4)]
                    
                    if pieces == [None, None, None]:
                        return self.QUEENSIDE
            

            kingside_rook = board.get_piece_from_pos((7, y))

            if kingside_rook != None:
                if not kingside_rook.has_moved:
                    pieces = [board.get_piece_from_pos((i, 7)) for i in range(5, 7)]

                    if pieces == [None, None]:
                        return self.KINGSIDE


    def get_valid_moves(self, board) -> List[Any]:
        valid_moves = []

        for square in self.get_moves(board):
            if not board.is_in_check(self.color, board_change=[self.pos, square.pos]):
                valid_moves.append(square)
            
            can_castle = self.can_castle(board)
            
            if can_castle == self.QUEENSIDE:
                valid_moves.append(board.get_square_from_pos((self.x - 2, self.y)))
            elif can_castle == self.KINGSIDE:
                valid_moves.append(board.get_square_from_pos((self.x + 2, self.y)))
            
            return valid_moves
