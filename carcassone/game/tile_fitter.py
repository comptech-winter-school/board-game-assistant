from typing import Set

from .carcassonne_game_state import CarcassonneGameState
from .side import Side
from .tile import Tile


class TileFitter:

    @classmethod
    def grass_fits(cls, center: Tile, top: Tile = None, right: Tile = None, bottom: Tile = None,
                   left: Tile = None) -> bool:
        for side in center.grass:
            if side == Side.LEFT and left is not None and not left.grass.__contains__(Side.RIGHT):
                return False
            if side == Side.RIGHT and right is not None and not right.grass.__contains__(Side.LEFT):
                return False
            if side == Side.TOP and top is not None and not top.grass.__contains__(Side.BOTTOM):
                return False
            if side == Side.BOTTOM and bottom is not None and not bottom.grass.__contains__(Side.TOP):
                return False
        return True

    @classmethod
    def cities_fit(cls, center: Tile, top: Tile = None, right: Tile = None, bottom: Tile = None, left: Tile = None) -> bool:
        for side in center.get_city_sides():
            if side == Side.LEFT and left is not None and not left.get_city_sides().__contains__(Side.RIGHT):
                return False
            if side == Side.RIGHT and right is not None and not right.get_city_sides().__contains__(Side.LEFT):
                return False
            if side == Side.TOP and top is not None and not top.get_city_sides().__contains__(Side.BOTTOM):
                return False
            if side == Side.BOTTOM and bottom is not None and not bottom.get_city_sides().__contains__(Side.TOP):
                return False
        return True

    @classmethod
    def roads_fit(cls, center: Tile, top: Tile = None, right: Tile = None, bottom: Tile = None, left: Tile = None) -> bool:
        for side in center.get_road_ends():
            if side == Side.LEFT and left is not None and not left.get_road_ends().__contains__(Side.RIGHT):
                return False
            if side == Side.RIGHT and right is not None and not right.get_road_ends().__contains__(Side.LEFT):
                return False
            if side == Side.TOP and top is not None and not top.get_road_ends().__contains__(Side.BOTTOM):
                return False
            if side == Side.BOTTOM and bottom is not None and not bottom.get_road_ends().__contains__(Side.TOP):
                return False
        return True

    
    @classmethod
    def fits(cls, center: Tile, top: Tile = None, right: Tile = None, bottom: Tile = None, left: Tile = None,
             game_state: CarcassonneGameState = None) -> bool:
        if top is None and right is None and bottom is None and left is None:
            return False

        return cls.grass_fits(center, top, right, bottom, left) \
               and cls.cities_fit(center, top, right, bottom, left) \
               and cls.roads_fit(center, top, right, bottom, left) 