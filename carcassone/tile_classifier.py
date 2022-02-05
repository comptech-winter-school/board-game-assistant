from PIL import Image
import torchvision.transforms as transforms
import torch
from torchvision.models import resnet18
from .base_deck import base_tiles
from .tilenames import class_names

class TilesClassifier:
    def __init__(self, model_path):
        self.classes = class_names
        self.model = resnet18()
        self.model.fc = torch.nn.Linear(512, len(self.classes))
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        self.transform  = transforms.Compose([
                                    transforms.Resize((128, 128)),
                                    transforms.ToTensor(), 
                                    transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                                        std=[0.229, 0.224, 0.225])])

    def classify(self, tile: Image):
        self.model.eval()
        tile_img = self.transform(tile)
        outputs = self.model(tile_img.unsqueeze(0))
        _, predicted = torch.max(outputs, dim=1)
        classname = self.classes[predicted.item()]
        if classname.split('_')[-1].isdigit():
            digit = classname.split('_')[-1]
            tile = base_tiles["_".join(classname.split('_')[:-1])]
            if digit == '90':
                tile = tile.turn(1)
                tile.image = tile.image.split('.')[0] + '_90.png'
            elif digit == '180':
                tile = tile.turn(2)
                tile.image =  tile.image.split('.')[0] + '_180.png'
            elif digit == '270':
                tile = tile.turn(3)
                tile.image = tile.image.split('.')[0] +'_270.png'
        else:
            tile = base_tiles[classname]
    
        return tile