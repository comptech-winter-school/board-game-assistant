import cv2
import json
from PIL import Image
from tgbot import tgbot
from gameClassifier import gameClassifier
from tictactoe import pipeline
from checkers import checkersDetector
from carcassone import tiles_board


detector = checkersDetector.CheckersDetector(pathToYolo='checkers/yolov5', pathToModel='checkers/models/detector.pt')


def detect_tictactoe(image_path, chat_id):
	result = pipeline.execute_pipline(image_path=image_path)
	print(len(result))
	if result[0] == 'Cannot detect game properly':
		bot.send_message(chat_id=chat_id, text='Unable to recognize game situation')
	else:
		cv2.imwrite("ttt.jpg", result[0])
		bot.send_photo(chat_id=chat_id, photo=open("ttt.jpg", 'rb'))


def detect_checkers(image_path, chat_id, top_white):
	img = cv2.imread(image_path)
	visual, layout, res_white, res_black  = detector.getGameField(img,visualize=True, roll=top_white)

	cv2.imwrite("layout.jpg", layout)
	bot.send_message(chat_id=chat_id, text='Detected layout:')
	bot.send_photo(chat_id=chat_id, photo=open("layout.jpg", 'rb'))

	cv2.imwrite("game.jpg", visual)
	bot.send_message(chat_id=chat_id, text='Digitized game:')
	bot.send_photo(chat_id=chat_id, photo=open("game.jpg", 'rb'))

	cv2.imwrite("res_white.jpg", res_white)
	bot.send_message(chat_id=chat_id, text='Suggested white move:')
	bot.send_photo(chat_id=chat_id, photo=open("res_white.jpg", 'rb'))
	
	cv2.imwrite("res_black.jpg", res_black)
	bot.send_message(chat_id=chat_id, text='Suggested black move:')
	bot.send_photo(chat_id=chat_id, photo=open("res_black.jpg", 'rb'))


def detect_carcassone(field_image_path, card_image_path, chat_id):
	field_image = Image.open(field_image_path)
	card_image = Image.open(card_image_path)

	board = tiles_board.CarcassoneBoard('carcassone/models/detection_model.pt', 'carcassone/models/cls_model.pt')
	board_img = board.recognize_game_situation(field_image)

	cv2.imwrite("board_img.jpg", board_img)
	bot.send_message(chat_id=chat_id, text='Detected board:')
	bot.send_photo(chat_id=chat_id, photo=open("board_img.jpg", 'rb'))

	positions_im, tile_im = board.get_possible_positions(card_image)
	
	tile_im.save("tile_im.jpg")
	bot.send_message(chat_id=chat_id, text='Detected tile:')
	bot.send_photo(chat_id=chat_id, photo=open("tile_im.jpg", 'rb'))

	cv2.imwrite("positions_im.jpg", positions_im)
	bot.send_message(chat_id=chat_id, text='Available tile positions:')
	bot.send_photo(chat_id=chat_id, photo=open("positions_im.jpg", 'rb'))

	tiles_left_im = board.get_tiles_left()
	tiles_left_im.save("tiles_left_im.jpg")
	bot.send_message(chat_id=chat_id, text='Tiles available:')
	bot.send_photo(chat_id=chat_id, photo=open("tiles_left_im.jpg", 'rb'))


if __name__ == "__main__":
	with open('config.json') as f:
		config = json.load(f)

	BOT_TOKEN = config['TG_BOT_KEY']

	handlers_fns = {
		'classifyGame': gameClassifier.classifyGameImage, 
		'detect_checkers': detect_checkers,
		'detect_tictactoe': detect_tictactoe,
		'detect_carcassone': detect_carcassone
	}
	bot = tgbot.initBot(token=BOT_TOKEN, handlers_fns=handlers_fns)
