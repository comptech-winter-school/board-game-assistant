from .tile_detector import TilesDetector
from .tile_classifier import TilesClassifier
from .game.carcassonne_game_state import CarcassonneGameState
from .tile_position_finder import TilePositionFinder
import numpy as np
from PIL import Image, ImageDraw
from .base_deck import base_tiles


class FailedToRecognizeError(Exception):
    pass


class CarcassoneBoard:
    def __init__(self, det_model_path, cls_model_path):
        self.board_detector = TilesDetector(det_model_path)
        self.tile_classifier = TilesClassifier(cls_model_path)
        self.tiles_locations = []
        self.meep_locations = []
        self.tiles_classes = []
        self.game_state = CarcassonneGameState()

    def recognize_game_situation(self, img: Image):
        tiles_imgs, self.tiles_locations, self.meep_locations = self.board_detector.detect(img)
        self.tiles = [self.tile_classifier.classify(tile) for tile in tiles_imgs]
        for tile, location in zip(self.tiles, self.tiles_locations):
            self.game_state.add_tile(location[0], location[1], tile)

        return self.draw()

    def recognize_tile(self, tile_img: Image):
        tile_img, _, _ = self.board_detector.detect(tile_img)
        if len(tile_img) != 1:
            return None
        tile = self.tile_classifier.classify(tile_img[0])
        return tile

    def draw(self):
        min_y, min_x, max_y, max_x = self.game_state.get_min_max_coord()
        tile_size = 64
        width = (max_x - min_x + 1) * tile_size
        height = (max_y - min_y + 1) * tile_size
        img = np.zeros((height, width, 3), dtype=np.uint8)
        for i in range(min_y, max_y + 1):
            for j in range(min_x, max_x + 1):
                if self.game_state.board[i][j] is not None:
                    coord_x = j - min_x
                    coord_y = i - min_y
                    tile = self.game_state.board[i][j]
                    tile_img = Image.open('carcassone/' + tile.image)
                    tile_img = np.asarray(tile_img.resize((tile_size, tile_size)))
                    img[coord_y * 64:(coord_y + 1) * tile_size,
                    coord_x * tile_size:(coord_x + 1) * tile_size] = tile_img

        return img

    def get_tiles_left(self):
        tile_counts = self.game_state.tile_counts
        start_top = 20
        start_left = 20
        tile_size = 64
        interval_y = 15
        interval_x = tile_size * 4
        tile_count_x = 2
        tile_count_y = 12
        text_int = 10
        image = Image.new('RGB', (tile_size * tile_count_x + interval_x * tile_count_x + start_left,
                                  tile_size * tile_count_y + start_top * 2 + interval_y * (tile_count_y - 1)),
                          (0, 0, 0))

        for j in range(tile_count_x):
            for i, tile_class in enumerate(list(base_tiles.keys())[tile_count_y * j:tile_count_y * (j + 1)]):
                tile_img = Image.open('carcassone/' + base_tiles[tile_class].image)
                tile_img = tile_img.resize((tile_size, tile_size))
                left = start_left + tile_size * j + interval_x * j
                right = left + tile_size
                top = start_top + tile_size * i + interval_y * i
                bottom = top + tile_size
                image.paste(tile_img, (left, top, right, bottom))

        image_draw = ImageDraw.Draw(image)

        for j in range(tile_count_x):
            for i, tile_class in enumerate(list(base_tiles.keys())[tile_count_y * j:tile_count_y * (j + 1)]):
                left = start_left + tile_size * j + interval_x * j
                right = left + tile_size
                top = start_top + tile_size * i + interval_y * i
                bottom = top + tile_size
                image_draw.text((right + text_int, top + text_int), tile_class, (237, 230, 211))
                tiles_left_text = f'tiles: {tile_counts[tile_class]}'
                image_draw.text((right + text_int, top + text_int + 20), tiles_left_text, (237, 230, 211))
        return image

    def get_possible_positions(self, new_tile_img: Image):
        new_tile = self.recognize_tile(new_tile_img)
        if new_tile is None:
            raise FailedToRecognizeError

        positions = TilePositionFinder.possible_playing_positions(self.game_state, new_tile)
        min_y, min_x, max_y, max_x = self.game_state.get_min_max_coord()
        tile_size = 64
        width = (max_x - min_x + 3) * tile_size
        height = (max_y - min_y + 3) * tile_size

        pos_img = np.zeros((height, width, 3), dtype=np.uint8)
        for i in range(min_y, max_y + 1):
            for j in range(min_x, max_x + 1):
                if self.game_state.board[i][j] is not None:
                    coord_x = j - min_x + 1
                    coord_y = i - min_y + 1
                    tile = self.game_state.board[i][j]
                    tile_img = Image.open('carcassone/' + tile.image)
                    tile_img = np.asarray(tile_img.resize((tile_size, tile_size)))
                    pos_img[coord_y * tile_size:(coord_y + 1) * tile_size,
                    coord_x * tile_size:(coord_x + 1) * tile_size] = tile_img

        for tile_position in positions:
            coord_y = tile_position.coordinate.row - min_y + 1
            coord_x = tile_position.coordinate.column - min_x + 1
            pos_img[coord_y * tile_size:(coord_y + 1) * tile_size,
            coord_x * tile_size:(coord_x + 1) * tile_size] = np.array([173, 255, 47])

        new_tile_def_img = Image.open('carcassone/' + new_tile.image).resize((512, 512))
        return pos_img, new_tile_def_img