import numpy as np
import pathlib
import re
import torch
from fastai.vision.all import *
from shutil import copy
from torch.nn.functional import softmax

pathlib.WindowsPath = pathlib.PosixPath


def classifyGameImage(image_path):
    dl = game_model.dls.test_dl([image_path], num_workers=0, bs=1)
    game_model.model.eval()

    with torch.no_grad():
      for batch in dl:
        out = game_model.model(batch[0])
        for item in out:
          if max(softmax(item)) > 0.95:
            prediction = str(game_model.dls.categorize.decode(np.argmax(softmax(item))))
          else:
            prediction = 'unknown'
  
          return prediction


model_path = 'gameClassifier/gameClassifier_v1.pkl'
game_model = load_learner(model_path, cpu=True)
