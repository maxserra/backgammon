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
        self.whoseTurn = blackPlayer
        input("Press enter to start playing")
        self.mainLoop()
        
    def mainLoop(self):
        while self.gameFinished == False:
            # Generate the dice rolls
            a = random.randint(1,6); b = random.randint(1,6)
            # Show the board
            self.board.display()
            player = "Black" if self.whoseTurn == blackPlayer else "White"
            print(f"{player} dice rolled {a} and {b}! \nMoves format: 'from,to;from,to;from,to;from,to'")
            # Get moves
            while True:
                try:
                    # Get the next moves
                    moves = input(f"What are {player} moves? ")
                    # Parse the moves into array format
                    moves = BackgammonParser().strToArray(moves)
                    print(moves)
                    # Check validity of the moves
                    # TODO
                    break
                # Allow ctrl+C to exit
                except KeyboardInterrupt:
                    exit(0)
                # Catch any other Exception
                except:
                    pass
                print("Invalid moves, try again...")
            # Apply moves to the board
            self.board.applyMoves(self.whoseTurn, moves)
            # Switch player
            self.whoseTurn *= -1

class BackgammonBoard():
    
    def __init__(self) -> None:
        self.positions = self.initialPositions()
        self.blacksHome = 0
        self.whitesHome = 0
        
    def initialPositions(self):
        return np.array([0, 
                         blackPlayer*2,            0,0,0,            0,whitePlayer*5,
                                     0,whitePlayer*3,0,0,            0,blackPlayer*5,
                         whitePlayer*5,            0,0,0,blackPlayer*3,            0,
                         blackPlayer*5,            0,0,0,            0,whitePlayer*2,
                         0])
        
    def getPositions(self) -> np.ndarray:
        return self.positions
    
    def setPositions(self, newPositions: np.ndarray):
        self.positions = newPositions
        
    def applyMoves(self, player: int, moves: np.ndarray):
        for i in range(len(self.positions)):
            # If taking pieces
            if moves[i] < 0:
                self.positions[i] = self.positions[i] + player * moves[i]
            # If putting pieces to home
            elif moves[i] > 0 and i in [0,25]:
                # Black putting home
                if i == 25:
                    self.blacksHome += 1
                # White putiing home
                elif i == 0:
                    self.whitesHome += 1
            # If putting pieces to own or empty field
            elif moves[i] > 0 and self.positions[i]/player >= 0:
                self.positions[i] = self.positions[i] + player * moves[i]
            # If putting pieces to contrary field
            elif moves[i] > 0 and self.positions[i]/player < 0:
                # If whites gets kicked
                if player == blackPlayer:
                    self.positions[25] += whitePlayer
                    self.positions[i] = player * moves[i]
                # If blacks gets kicked
                if player == whitePlayer:
                    self.positions[0] += blackPlayer
                    self.positions[i] = player * moves[i]
        
    def display(self):
        print("|                                        | 1 | 1 | 1 |")
        print("| 0 || 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | 1 | 2 |")
        print("|---++---+---+---+---+---+---+---+---+---+---+---+---|")
        for i in range(5):
            #print("|   |", end="")
            for j in range(0,13):
                if abs(self.positions[j]) > i and self.positions[j]/blackPlayer > 0:
                    print("| B ", end="")
                elif abs(self.positions[j]) > i and self.positions[j]/whitePlayer > 0:
                    print("| W ", end="")
                else:
                    print("|   ", end="")
                if j == 0:
                    print("|", end="")
            print("|")
        print("|----------------------------------------------------|")
        for i in range(5):
            #print("|   |", end="")
            for j in range(25,12,-1):
                if abs(self.positions[j]) > 4-i and self.positions[j]/blackPlayer > 0:
                    print("| B ", end="")
                elif abs(self.positions[j]) > 4-i and self.positions[j]/whitePlayer > 0:
                    print("| W ", end="")
                else:
                    print("|   ", end="")
                if j == 25:
                    print("|", end="")
            print("|")
        print("|---++---+---+---+---+---+---+---+---+---+---+---+---|")
        print("| 2 || 2 | 2 | 2 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |")
        print("| 5 || 4 | 3 | 2 | 1 | 0 | 9 | 8 | 7 | 6 | 5 | 4 | 3 |")

class BackgammonParser():
    
    def __init__(self) -> None:
        pass
    
    def strToArray(self, moves: str) -> np.ndarray:
        # Create return array
        arrMoves = np.zeros(26)
        # Split input
        moves = moves.split(";")
        # Check number of moves. Must be either 2 or 4
        if len(moves) not in [2,4]:
            raise ValueError
        # Check moves format and type
        for i in range(len(moves)):
            move = moves[i].split(",")
            # Check that each move is complete
            if len(move) != 2:
                raise ValueError
            # Try to cast the move
            try:
                moveFrom, moveTo = [int(val) for val in move]
            except:
                raise TypeError
            # Check range
            if moveFrom not in range(26) and moveTo not in range(26):
                raise ValueError
            # Implement move to arrMoves
            arrMoves[moveFrom] -= 1
            arrMoves[moveTo]   += 1
        # Return array
        return arrMoves

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