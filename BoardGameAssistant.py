import cv2
import json
from tgbot import tgbot
from gameClassifier import gameClassifier
from checkers import checkersDetector

detector = checkersDetector.CheckersDetector(pathToYolo='checkers/yolov5', pathToModel='checkers/models/detector.pt')

def detect_checkers(image_path, chat_id):
	img = cv2.imread(image_path)
	visual, layout, res_white, res_black  = detector.getGameField(img,visualize=True)
	cv2.imwrite("layout.jpg", layout)
	cv2.imwrite("game.jpg", visual)
	cv2.imwrite("res_white.jpg", res_white)
	cv2.imwrite("res_black.jpg", res_black)
	bot.send_message(chat_id=chat_id, text='Detected layout:')
	bot.send_photo(chat_id=chat_id, photo=open("layout.jpg", 'rb'))
	bot.send_message(chat_id=chat_id, text='Digitized game:')
	bot.send_photo(chat_id=chat_id, photo=open("game.jpg", 'rb'))
	bot.send_message(chat_id=chat_id, text='Suggested white move:')
	bot.send_photo(chat_id=chat_id, photo=open("res_white.jpg", 'rb'))
	bot.send_message(chat_id=chat_id, text='Suggested black move:')
	bot.send_photo(chat_id=chat_id, photo=open("res_black.jpg", 'rb'))

CONFIG_PATH = "config.json"
with open(CONFIG_PATH) as f:
	config = json.load(f)

BOT_TOKEN = config['TG_BOT_KEY']
bot = tgbot.initBot(token=BOT_TOKEN, classifyGameFunction=gameClassifier.classifyGameImage, detect_checkersFunction=detect_checkers)
