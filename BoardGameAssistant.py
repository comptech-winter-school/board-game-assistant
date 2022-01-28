import json
from tgbot import tgbot
from gameClassifier import gameClassifier

CONFIG_PATH = "config.json"
with open(CONFIG_PATH) as f:
	config = json.load(f)

BOT_TOKEN = config['TG_BOT_KEY']

tgbot.initBot(token=BOT_TOKEN, classifyGameFunction=gameClassifier.classifyGameImage)
