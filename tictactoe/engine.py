import cv2
import random

from time import sleep
from random import randint
from .gameboard import Gameboard
PLAYERS = ["X", "O"]


class GameEngine(object):
    def __init__(self, currentplayer, debug=100):
        self.gameboard = ["?"] * 9
        self.currentbuffer = 0
        self._gameboard = None  # temporary variable for opencv board
        self.save_gameboard = None

        self.moves = []
        self.diff = None
        self.debug = debug
        self._winning_combinations = (
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6])
        self.player, self.ai_player = self._ask_player_letter(currentplayer)
        self.currentplayer = self.ai_player

    def _is_board_empty(self):
        unique = list(set(self._gameboard.status()))
        if (len(unique) == 1) and unique[0] == "?":
            return True
        return False

    def _is_game_won(self):
        for player in PLAYERS:
            for combos in self._winning_combinations:
                if (self.gameboard[combos[0]] == player and self.gameboard[combos[1]] == player and self.gameboard[
                    combos[2]] == player):
                    return player
        if "?" not in self.gameboard:
            return "tie"
        return None

    def _is_game_won_player(self, player, board):
        for combos in self._winning_combinations:
            if (board[combos[0]] == player and board[combos[1]] == player and board[combos[2]] == player):
                return True

        return False

    def _get_free_position(self):
        board = self.gameboard
        free = [i for i, pos in enumerate(board) if pos == "?"]
        return random.choice(free)

    def _get_all_free_pos(self, board):
        free = [i for i, pos in enumerate(board) if pos == "?"]
        return free

    def _decide_initial_player(self):
        return random.choice(PLAYERS)

    def _ask_player_letter(self, currentplayer):
        player = currentplayer
        if (player.lower() == "x"):
            player = "X"
            ai_player = "O"
        else:
            player = "O"
            ai_player = "X"
        return player, ai_player

    def _is_move_valid(self, move):
        pos = -1
        try:
            pos = int(move)
        except:
            return None
        if self.gameboard[pos] == "?":
            return pos
        return None

    def _update_board(self, pos, player):
        self.gameboard[pos] = player
        self._gameboard.positions[pos].draw_symbol_on_position(player, pos)

    def update_ai_board(self, pos, player, board):
        board[pos] = player
        return board

    def _ask_player_move(self):
        valid = False
        before = self.gameboard
        while not valid:
            pos = input("Enter position [0-8]: ")
            valid_pos = self._is_move_valid(pos)
            if (valid_pos != None):
                valid = True
                self._update_board(valid_pos, self.player)
                self.currentplayer = self.ai_player

    def _make_move(self):
        self._ai_make_move()

    def init_gameboard_ai(self):
        # board = ["X", "?", "?", "O", "?", "O", "?", "X", "?"]
        board = 9 * ["?"]
        self.gameboard = board
        return board

    def _change_player(self, player):
        if player == "X":
            return "O"
        else:
            return "X"

    def minimax(self, newBoard, player):
        available_pos = self._get_all_free_pos(newBoard)
        if self._is_game_won_player("X", newBoard):
            score = 0
            return score
        elif self._is_game_won_player("O", newBoard):
            score = 100
            return score
        elif len(available_pos) == 0:
            score = 50
            return score

        if player == "O":
            bestVal = 0
            for var in available_pos:
                # print("Making move: " + str(var))
                newBoard = self.update_ai_board(var, player, newBoard)
                moveVal = self.minimax(newBoard, "X")
                newBoard = self.update_ai_board(var, "?", newBoard)
                bestVal = max(bestVal, moveVal)
            return bestVal

        if player == "X":
            bestVal = 100
            for var in available_pos:
                # print("Making move: " + str(var))
                newBoard = self.update_ai_board(var, player, newBoard)
                moveVal = self.minimax(newBoard, "O")
                newBoard = self.update_ai_board(var, "?", newBoard)
                bestVal = min(bestVal, moveVal)
            return bestVal

    def make_best_move(self, board, player, difficulty):
        if difficulty == "Easy":
            diff_random = 25
        elif difficulty == "Medium":
            diff_random = 50
        elif difficulty == "Hard":
            diff_random = 75
        else:
            diff_random = 100
        # Generate random
        rnum = randint(0, 100)
        # Find available moves
        initValue = 50
        best_choices = []

        available_pos = self._get_all_free_pos(board)
        if len(available_pos) == 9 and diff_random == 100:
            return 4
        if rnum > diff_random:
            move = random.choice(available_pos)
            return move

        else:
            if player == "O":
                for move in available_pos:
                    board = self.update_ai_board(move, player, board)
                    moveVal = self.minimax(board, self._change_player(player))
                    board = self.update_ai_board(move, "?", board)

                    if moveVal > initValue:
                        best_choices = [move]
                        return move
                    elif moveVal == initValue:
                        best_choices.append(move)
            else:
                for move in available_pos:
                    board = self.update_ai_board(move, player, board)
                    moveVal = self.minimax(board, self._change_player(player))
                    board = self.update_ai_board(move, "?", board)

                    if moveVal < initValue:
                        best_choices = [move]
                        return move
                    elif moveVal == initValue:
                        best_choices.append(move)

            if len(best_choices) > 0:
                return random.choice(best_choices)
            else:
                return random.choice(available_pos)

    def _ai_make_move(self):
        origBoard = self.gameboard
        pos = self.make_best_move(origBoard, self.ai_player, self.diff)
        # print("Best: ", pos)
        self._update_board(pos, self.ai_player)
        self.currentplayer = self.player

    def show_gameboard(self):
        t = self.gameboard
        print("{0} {1} {2}".format(t[0], t[1], t[2]))
        print("{0} {1} {2}".format(t[3], t[4], t[5]))
        print("{0} {1} {2}".format(t[6], t[7], t[8]))

    def _parse_gameboard(self, gameboard_file):
        image = cv2.imread(gameboard_file)
        self._gameboard = Gameboard.detect_game_board(image, debug=self.debug)

    def is_winner(self, use_camera=False, gameboard_file="images/one_average_x.jpg"):
        self._parse_gameboard(gameboard_file)
        self.gameboard = self._gameboard.status()
        winner = self._is_game_won()
        return winner, self.ai_player


    def start(self, use_camera=False, gameboard_file="images/one_average_x.jpg"):
        self._parse_gameboard(gameboard_file)
        self.gameboard = self._gameboard.status()
        self.save_gameboard = self.gameboard.copy()
        # self.show_gameboard()
        # print("==========")
        # if not self._is_board_empty():
        #     raise Exception("Board is not empty. Please clear board.")

        # Print board status
        # ai_player = self.ai_player
        # hu_player = self.player
        # print(ai_player, hu_player)
        #difficulty = int(input(" 1: Easy \n 2: Medium \n 3: Hard \n 4: Expert \n Choose a difficulty: "))
        # if difficulty == 1:
        #     self.diff = "Easy"
        # elif difficulty == 2:
        #     self.diff = "Medium"
        # elif difficulty == 3:
        #     self.diff = "Hard"
        # else:
        self.diff = "Expert"
        if self._is_game_won() is None:
            # for self.ai_player, self.player in [("X", "O"), ("O", "X")]:
            try:
                self._parse_gameboard(gameboard_file)
            except Exception as e:
                print("Unable to detect game board.")
                sleep(1)
            # print("Your move player {0}".format(self.currentplayer))
            # pdb.set_trace()
            self._make_move()
            # self.show_gameboard()
        winner = self._is_game_won()
        if winner == "tie":
            return self.gameboard, self.save_gameboard, True, "A TIE!"
        elif winner == self.player:
            return self.gameboard, self.save_gameboard, True, self.ai_player
        elif winner == self.ai_player:
            return self.gameboard, self.save_gameboard, True, self.ai_player
        return self.gameboard, self.save_gameboard, False, None

