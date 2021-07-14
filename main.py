import numpy as np
import random
import sys

blackPlayer = -1
whitePlayer = +1

class BackgammonGame():
    
    def __init__(self) -> None:
        print("Welcome to Backgammon!")
        self.board = BackgammonBoard()
        self.gameFinished = False
        self.nextPlayer = blackPlayer
        input("Press enter to start playing")
        self.mainLoop()
        
    def mainLoop(self):
        while self.gameFinished == False:
            # Generate the dice rolls
            a = random.randint(1,6); b = random.randint(1,6)
            # Show the board
            self.board.display()
            nextPlayer = "Black" if self.nextPlayer == blackPlayer else "White"
            print(f"{nextPlayer} dice rolled {a} and {b}! \nMoves format: 'from,to;from,to;from,to;from,to'")
            # Get moves
            while True:
                try:
                    c = input(f"What are {nextPlayer} moves? ")
                    if c == "special":
                        break
                except KeyboardInterrupt:
                    exit(0)
                    
                print("Invalid moves, try again...")
            
            # Switch player
            self.nextPlayer *= -1

class BackgammonBoard():
    
    def __init__(self) -> None:
        self.positions = self.initialPositions()
        
    def initialPositions(self):
        return np.array([[blackPlayer,2],[          0,0],[0,0],[0,0],[          0,0],[whitePlayer,5],
                         [ 0         ,0],[whitePlayer,3],[0,0],[0,0],[          0,0],[blackPlayer,5],
                         [whitePlayer,5],[          0,0],[0,0],[0,0],[blackPlayer,3],[          0,0],
                         [blackPlayer,5],[          0,0],[0,0],[0,0],[          0,0],[whitePlayer,2]])
        
    def getPositions(self) -> np.ndarray:
        return self.positions
    
    def setPositions(self, newPositions: np.ndarray):
        self.positions = newPositions
        
    def display(self):
        print("|                                        | 1 | 1 | 1 |")
        print("| 0 || 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | 1 | 2 |")
        print("|---++---+---+---+---+---+---+---+---+---+---+---+---|")
        for i in range(5):
            print("|   |", end="")
            for j in range(12):
                if self.positions[j][1] > i and self.positions[j][0] == blackPlayer:
                    print("| B ", end="")
                elif self.positions[j][1] > i and self.positions[j][0] == whitePlayer:
                    print("| W ", end="")
                else:
                    print("|   ", end="")
            print("|")
        print("|----------------------------------------------------|")
        for i in range(5):
            print("|   |", end="")
            for j in range(23,11,-1):
                if self.positions[j][1] > 4-i and self.positions[j][0] == blackPlayer:
                    print("| B ", end="")
                elif self.positions[j][1] > 4-i and self.positions[j][0] == whitePlayer:
                    print("| W ", end="")
                else:
                    print("|   ", end="")
            print("|")
        print("|---++---+---+---+---+---+---+---+---+---+---+---+---|")
        print("| 2 || 2 | 2 | 2 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |")
        print("| 5 || 4 | 3 | 2 | 1 | 0 | 9 | 8 | 7 | 6 | 5 | 4 | 3 |")

class BackgammonRules():
    
    def __init__(self) -> None:
        pass
    
    def checkMove(self, positions: np.ndarray, player: int, moveFrom: int, moveTo: int) -> bool:
        # Check boundary conditions
        if player != blackPlayer and player != whitePlayer:
            return False
        if moveTo > 25 or moveFrom < 0:
            return False
        if abs(moveTo - moveFrom) > 6:
            return False
        # Check direction
        if player == blackPlayer and moveFrom > moveTo:
            return False
        if player == whitePlayer and moveFrom < moveTo:
            return False
        # Check if origin belongs to player
        if positions[moveFrom][0] != player:
            return False
        # Check if target belongs to player and has 5+
        if positions[moveTo][0] == player and positions[moveTo][1] >= 5:
            return False
        # Check if target belongs to oponent and has 2+
        if positions[moveTo][0] == -player and positions[moveTo][1] >= 2:
            return False
        # Check if moving 'out' is allowed - black
        if player == blackPlayer and moveTo == 25:
            # Check if all pieces are in the last 6 positions
            if blackPlayer in positions[:19,0]:
                return False
        # Check if moving 'out' is allowed - white
        if player == whitePlayer and moveTo == 0:
            # Check if all pieces are in the last 6 positions
            if whitePlayer in positions[6:,0]:
                return False
        
        # The move is valid
        return True

BackgammonGame()