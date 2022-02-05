import cv2
import numpy as np

from .gamevalidator import validate_conditions
from .gameboard import Gameboard
from .engine import GameEngine


def pipeline(image_path: str = ""):

    image = cv2.imread(image_path)
    gameboard = Gameboard.detect_game_board(image, debug=0)
    status = gameboard.status()
    cnt, status_bool = validate_conditions(status)
    if status_bool is False:
        return ["GAME IS NOT VALID!"]

    ge = GameEngine(currentplayer="X", debug=0)
    winner, _ = ge.is_winner(gameboard_file=image_path)
    output = []
    if winner:
        output.append(f"GAME OVER! THE WINNER IS '{winner}'!")
        return output

    if cnt.get("X", 0) < cnt.get("O", 0):
        output = []
        ge = GameEngine(currentplayer="O", debug=0)
        board_output, saved_board, is_game_finished, winner = ge.start(gameboard_file=image_path)
        if is_game_finished:
            if winner == "A TIE!":
                output.append("GAME OVER! IT WAS A TIE!")
            else:
                output.append([board_output, saved_board])
        else:
            output.append([board_output, saved_board])
        return output
    elif cnt.get("X", 0) > cnt.get("O", 0):
        output = []
        ge = GameEngine(currentplayer="X", debug=0)
        board_output, saved_board, is_game_finished, winner = ge.start(gameboard_file=image_path)
        if is_game_finished:
            if winner == "A TIE!":
                output.append("GAME OVER! IT WAS A TIE!")
            else:
                output.append([board_output, saved_board])
        else:
            output.append([board_output, saved_board])
        return output
    else:
        output = []
        ge = GameEngine(currentplayer="X", debug=0)
        board_output, saved_board, is_game_finished, winner = ge.start(gameboard_file=image_path)
        if is_game_finished:
            if winner == "A TIE!":
                output.append("GAME OVER! IT WAS A TIE!")
            else:
                output.append([board_output, saved_board])
        else:
            output.append([board_output, saved_board])
        ge = GameEngine(currentplayer="O", debug=0)
        board_output, saved_board, is_game_finished, winner = ge.start(gameboard_file=image_path)
        if is_game_finished:
            if winner == "A TIE!":
                output.append("GAME OVER! IT WAS A TIE!")
            else:
                output.append([board_output, saved_board])
        else:
            output.append([board_output, saved_board])
        return output

def drawer(out1, out2):
    centers = {
        0: (20, 20),
        1: (60, 20),
        2: (100, 20),
        3: (20, 60),
        4: (60, 60),
        5: (100, 60),
        6: (20, 100),
        7: (60, 100),
        8: (100, 100),

    }
    img = np.full((120, 120, 3), fill_value=255).astype(np.int32)
    img = cv2.line(img, (0, 40), (120, 40), (0, 0, 0), 1)
    img = cv2.line(img, (0, 80), (120, 80), (0, 0, 0), 1)
    img = cv2.line(img, (40, 0), (40, 120), (0, 0, 0), 1)
    img = cv2.line(img, (80, 0), (80, 120), (0, 0, 0), 1)
    i = 0
    for char1, char2 in zip(out1, out2):
        if char1 == char2:
            if char1 == "X":
                cv2.drawMarker(img, centers[i], (255, 0, 0),
                               markerType=cv2.MARKER_TILTED_CROSS, markerSize=20, thickness=1, line_type=cv2.LINE_8)
            elif char1 == "O":
                cv2.circle(img, centers[i], 10, (0, 255, 0), thickness=1)
        else:
            if char1 == "X":
                cv2.drawMarker(img, centers[i], (0, 0, 255),
                               markerType=cv2.MARKER_TILTED_CROSS, markerSize=20, thickness=1, line_type=cv2.LINE_8)
            elif char1 == "O":
                cv2.circle(img, centers[i], 10, (0, 0, 255), thickness=1)
        i += 1
    return img

def write_text(text):
    img = np.full((40, 220, 3), fill_value=255).astype(np.int32)
    font = cv2.FONT_HERSHEY_SIMPLEX

    org = (2, 25)
    fontScale = 0.4
    color = (255, 0, 0)
    thickness = 1

    img = cv2.putText(img, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
    return img

def execute_pipline(image_path="5.jpg"):
    try:
        output_list = pipeline(image_path=image_path)
        telegram_output = []
        for output in output_list:
            if isinstance(output, list):
                image = drawer(output[0], output[1])
                # plt.imshow(image)
                # plt.show()
                telegram_output.append(image)
            else:
                image = write_text(output)
                # plt.imshow(image)
                # plt.show()
                telegram_output.append(image)
        return telegram_output
    except:
        return ["Cannot detect game properly"]
