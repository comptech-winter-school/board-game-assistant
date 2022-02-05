import numpy as np
import torch
from PIL import Image

class TilesDetector:
    def __init__(self, model_path):
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', 
                                    path=model_path, device='cpu')
        self.model.conf = 0.6
        self.detection_df = None

    def _get_tiles_locations(self, tile_df):
        xmin = tile_df.xmin
        xmax = tile_df.xmax
        ymin = tile_df.ymin
        ymax = tile_df.ymax
        tile_width = (xmax-xmin).mean()
        tile_height = (ymax-ymin).mean()

        n_bins_x = int(round((xmin.max()-xmin.min()) / tile_width) + 1)
        n_bins_y = int(round((ymin.max()-ymin.min()) / tile_height) + 1)
        counts_x, vals_x = np.histogram(xmin, bins=n_bins_x, range=(xmin.min()-1, xmin.max()+1))
        counts_y, vals_y = np.histogram(ymin, bins=n_bins_y, range=(ymin.min()-1, ymin.max()+1))
        y_coord = np.digitize(ymin, vals_y) - 1
        x_coord = np.digitize(xmin, vals_x) - 1
        coordinates = np.array((y_coord, x_coord)).T.reshape(-1, 2)
        return coordinates

    def _get_tiles(self, img, tile_df):
        tiles = []
        for tile_num in range(len(tile_df)):
            im = img.crop((tile_df.loc[tile_num].xmin, tile_df.loc[tile_num].ymin, 
                           tile_df.loc[tile_num].xmax, tile_df.loc[tile_num].ymax))
            tiles.append(im)
        return tiles

    def _get_meep_locations(self, meep_df):
        return None

    def detect(self, img: Image):
        self.detection_df = self.model(img, size=640).pandas().xyxy[0]
        tile_df = self.detection_df[self.detection_df['name'] == 'tile']
        meep_df = self.detection_df[self.detection_df['name'] == 'meep']
        tiles_locations = self._get_tiles_locations(tile_df)
        meep_locations = self._get_meep_locations(meep_df)
        tile_imgs = self._get_tiles(img, tile_df)
        return tile_imgs, tiles_locations, meep_locations