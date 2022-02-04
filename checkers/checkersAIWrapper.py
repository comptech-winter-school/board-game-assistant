from .PythonCheckersAI.checkers import board
from .PythonCheckersAI.checkers.board  import Board
from .PythonCheckersAI.checkers.piece import Piece
from .PythonCheckersAI.checkers.game import Game
from .PythonCheckersAI.checkers.constants import RED, WHITE
import numpy as np 


class CustomBoard(Board):
    
    def __init__(self, array, roll):
        self.board = [] 
        self.red_left = self.white_left = 0
        self.red_kings = self.white_kings = 0
        self.roll = roll
        for row in range(len(array)):
            self.board.append([])
            for column in range(len(array[row])):
                if array[row][column] == 1 :
                    if roll:
                        self.board[row].append(Piece(row,column,WHITE))
                        self.white_left += 1
                    else:
                        self.board[row].append(Piece(row,column,RED))
                        self.red_left += 1
                elif array[row][column] == 2:
                    if roll:
                        self.board[row].append(Piece(row,column,RED))
                        self.red_left += 1
                    else:
                        self.board[row].append(Piece(row,column,WHITE))
                        self.white_left += 1
                else:
                    self.board[row].append(0)
    
    def convertBoard(self):
        field = np.zeros(shape = (8,8)) 
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                if self.board[row][column] == 0:
                    continue
                if self.board[row][column].color == WHITE:
                    if self.roll :
                        field[row,column] = 1
                    else:    
                        field[row,column] = 2
                elif self.board[row][column].color == RED:
                    if self.roll:
                        field[row,column] = 2
                    else:
                        field[row,column] = 1

        return field
        
class CustomGame(Game):
    def __init__(self,win,field,roll):
        self.field = field
        self.roll = roll
        super().__init__(win)
        self.board = CustomBoard(self.field, self.roll)

    def reset(self):
        super().reset()
        self.board = CustomBoard(self.field,self.roll)
    


def main():
    board = Board()
    print(board.board)

if __name__ == "__main__":
    main()