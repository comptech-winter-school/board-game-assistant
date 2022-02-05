import random
from typing import Optional
from .tile_action import TileAction
from .coordinate import Coordinate
from .game_phase import GamePhase
from .rotation import Rotation
from .tile import Tile
from .tile_sets import TileSet
from ..base_deck import base_tile_counts

class CarcassonneGameState:

    def __init__(
            self,
            tile_sets = (TileSet.BASE, TileSet.THE_RIVER, TileSet.INNS_AND_CATHEDRALS),
            players: int = 2,
            board_size = (35, 35),
            starting_position: Coordinate = Coordinate(17, 17)
    ):
        self.board = [[None for column in range(board_size[1])] for row in range(board_size[0])]
        self.starting_position: Coordinate = starting_position
        self.players = players
        self.meeples = [7 for _ in range(players)]
        self.placed_meeples = [[] for _ in range(players)]
        self.scores = [0 for _ in range(players)]
        self.current_player = 0
        self.phase = GamePhase.TILES
        self.last_tile_action: Optional[TileAction] = None
        self.last_river_rotation: Rotation = Rotation.NONE
        self.tile_counts = base_tile_counts

    def add_tile(self, row: int, column: int, tile: Tile):
        row_pos = self.starting_position.row + row
        col_pos = self.starting_position.column + column

        if row_pos < 0:
            for i in range(-row_pos):
                self.board.insert(0, [])
                self.board.insert(0, [])
                self.starting_position.row -= 2
        elif row_pos == 0:
            for i in range(-row_pos):
                self.board.insert(0, [])
                self.starting_position.row -= 1
        elif row_pos > len(self.board) - 1:
            for i in range(row_pos - len(self.board) + 1):
                self.board.append([])
                self.board.append([])
        elif row_pos == len(self.board) - 1:
            for i in range(row_pos - len(self.board) + 1):
                self.board.append([])

        if col_pos < 0:
            for i in range(-col_pos):
                for row in self.board:
                    row.insert(0, None)
                    row.insert(0, None)
                self.starting_position.column -= 2
        elif col_pos == 0:
            for i in range(-col_pos):
                for row in self.board:
                    row.insert(0, None)
                self.starting_position.column -= 1
        elif col_pos > len(self.board[0])-1:
            for i in range(col_pos - len(self.board[0]) + 1):
                for row in self.board:
                    row.append(None)
                    row.append(None)
        elif col_pos == len(self.board[0])-1:
            for i in range(col_pos - len(self.board[0]) + 1):
                for row in self.board:
                    row.append(None)

        self.board[row_pos][col_pos] = tile
        self.tile_counts[tile.description] -= 1


    def get_tile(self, row: int, column: int):
        if row < 0 or column < 0:
            return None
        elif row >= len(self.board) or column >= len(self.board[0]):
            return None
        else:
            return self.board[row][column]

    def get_min_max_coord(self):
        col_ind = []
        row_ind = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] is not None:
                    col_ind.append(i)
                    row_ind.append(j)

        return min(col_ind), min(row_ind), max(col_ind), max(row_ind)

    def empty_board(self):
        for row in self.board:
            for column in row:
                if column is not None:
                    return False
        return True

    def is_terminated(self) -> bool:
        return self.next_tile is None

    def initialize_deck(self, tile_sets):
        deck = []
        new_tiles = []

        if TileSet.BASE in tile_sets:
            for card_name, count in base_tile_counts.items():
                for i in range(count):
                    new_tiles.append(base_tiles[card_name])

        random.shuffle(new_tiles)
        for tile in new_tiles:
            deck.append(tile)

        return deck