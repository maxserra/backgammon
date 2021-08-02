from operator import mul
import numpy as np
from sympy.utilities.iterables import multiset_permutations
import copy
import logging

logging.basicConfig(encoding="utf-8", level=logging.DEBUG, format="%(asctime)s: %(levelname)s: %(message)s", datefmt="%d/%m/%Y %H:%M:%S")

blackPlayer = -1
whitePlayer = +1

class BackgammonGame():
    
    def __init__(self) -> None:
        print("Welcome to Backgammon!")
        self.setStartingValues()
        input("Press enter to start playing")
        self.mainLoop()
    
    def setStartingValues(self):
        self.board = BackgammonBoard()
        self.gameFinished = False
        self.whoseTurn = blackPlayer
        
    def mainLoop(self):
        logging.info("Entering mainLoop()")
        while self.gameFinished == False:
            # Generate the dice rolls
            diceRolls = np.random.randint(1, 7, 2)
            logging.debug(f"Player: {self.whoseTurn} Dice rolls: {diceRolls}")
            # Show the board
            self.board.display()
            strPlayer = "Black" if self.whoseTurn == blackPlayer else "White"
            print(f"{strPlayer} dice rolled {diceRolls[0]} and {diceRolls[1]}! \nMoves format: 'from,to;from,to;from,to;from,to'")
            # Get moves
            while True:
                try:
                    # Get the next moves
                    strMoves = input(f"What are {strPlayer} moves? ")
                    logging.debug(f"Input moves: {strMoves}")
                    # Parse the moves into array format
                    arrMoves = BackgammonParser().strToArrayOfMoves(strMoves)
                    ## # Parse the array into array format (will be necessary later)
                    ## strMoves = BackgammonParser().tupleToArrayOfMoves(moves)
                    # Check validity of the moves
                    if BackgammonRules().checkMoves(self.board.positions, arrMoves, self.whoseTurn, diceRolls):
                        break
                # Allow ctrl+C to exit
                except KeyboardInterrupt:
                    exit(0)
                # Catch any other Exception
                except:
                    pass
                print("Invalid moves, try again...")
            # Apply moves to the board
            outcome = self.board.applyMoves(self.whoseTurn, arrMoves)
            # Handle end of the game
            if outcome == blackPlayer:
                self.gameFinished = True
                logging.info(f"Player {outcome} wins")
                print("Black player wins!!!")
            elif outcome == whitePlayer:
                self.gameFinished = True
                logging.info(f"Player {outcome} wins")
                print("Black player wins!!!")
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
        # Deep copy of given positions
        self.positions = copy.deepcopy(newPositions)
    
    def applyMoves(self, player: int, moves: np.ndarray) -> int:
        """Applies the given moves to the board, changing the positions of the pieces
        
        Parameters
        ----------
        player : int
            The player that does the moves
        moves : ndarray
            Array of shape (n,2,2) (or (n,4,2) when doubles are rolled) containign the moves.
            Where n is the number of possible move combinations
            Format: [[[from_0, to_0],
                      [from_1, to_1],
                     ([from_2, to_2],
                      [from_3, to_3])]]
        """
        # Apply the moves iteratively
        for move in moves[0]:
            self.applySingleMove(player, BackgammonParser().singleMoveToBoardMove(move))
        # Check if game is over
        if self.blacksHome == 15:
            return blackPlayer
        elif self.whitesHome == 15:
            return whitePlayer
        else:
            return 0
    
    def applySingleMove(self, player: int, move: np.ndarray):
        for i in range(len(self.positions)):
            # If taking pieces
            if move[i] < 0:
                self.positions[i] += player * move[i]
            # If putting pieces to home
            elif move[i] > 0 and i in [0, 25]:
                # Black putting home
                if i == 25:
                    self.blacksHome += 1
                # White putiing home
                elif i == 0:
                    self.whitesHome += 1
            # If putting pieces to own or empty field
            elif move[i] > 0 and np.sign(self.positions[i]) in [player, 0]:
                self.positions[i] += player * move[i]
            # If putting pieces to contrary field
            elif move[i] > 0 and np.sign(self.positions[i]) == -player:
                # If whites gets kicked
                if player == blackPlayer:
                    self.positions[25] += whitePlayer
                    self.positions[i] = player * move[i]
                # If blacks gets kicked
                if player == whitePlayer:
                    self.positions[0] += blackPlayer
                    self.positions[i] = player * move[i]
        
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
    
    def strToArrayOfMoves(self, strMoves: str) -> np.ndarray:
        """Converts moves from string to array format
        
        Parameters
        ----------
        strMoves : str
            String containing the moves 
            Format: ';' separates the single moves and ',' separate origin from destin
            
        Returns
        -------
        ndarray
            Array of shape (1,2,2) (or (1,4,2) when doubles are rolled) containign the moves
            Format: [[[from_0, to_0],
                      [from_1, to_1],
                     ([from_2, to_2],
                      [from_3, to_3])]]
        """
        # Split input
        moves = strMoves.split(";")
        # Check number of moves. Must be either 2 or 4
        if len(moves) not in [2,4]:
            logging.debug(f"Invalid moves format '{strMoves}'")
            raise ValueError
        # Create return array
        arrMoves = np.empty((1,len(moves),2), dtype=int)
        for i in range(len(moves)):
            move = moves[i].split(",")
            # Check that each move is complete
            if len(move) != 2:
                logging.debug(f"Invalid move format '{moves[i]}'")
                raise ValueError
            # Try to cast the move
            try:
                moveFrom, moveTo = [int(val) for val in move]
            except:
                logging.debug(f"Move '{move}' could not be casted to int")
                raise TypeError
            # Check range
            if moveFrom not in range(26) and moveTo not in range(26):
                logging.debug(f"Move '{move}' values are out of range")
                raise ValueError
            # Write move to arrMoves
            arrMoves[0,i,0] = moveFrom
            arrMoves[0,i,1] = moveTo
        # Return arrMoves
        return arrMoves
    
    def singleMoveToBoardMove(self, singleMove: np.ndarray) -> np.ndarray:
        """Converts a single move to board-move-array format
        
        Parameters
        ----------
        singleMove : ndarray
            Array of shape (2,) containing the move
            Format: [from, to]
        
        Returns
        -------
        ndarray
            Array of shape (26,) containg the move in boardMove representation
            Format: all zeros except for positions 'from' and 'to'. 'from' = -1 and 'to' = +1 
        """
        # Check shape of input
        if singleMove.shape != (2,):
            logging.debug(f"Invalid move format {singleMove}")
            raise ValueError
        # Try to cast the move
        try:
            singleMove = singleMove.astype(int)
        except:
            logging.debug(f"Move '{singleMove}' could not be casted to int")
            raise TypeError
        # Check range
        if singleMove[0] not in range(26) and singleMove[1] not in range(26):
            logging.debug(f"Move '{singleMove}' values are out of range")
            raise ValueError
        # Create return array
        boardMove = np.zeros(26)
        # Modify value of given positions
        boardMove[singleMove[0]] = -1
        boardMove[singleMove[1]] = +1
        # Return array
        return boardMove
    
    def tupleToArrayOfMoves(self, arrMoves: tuple[np.ndarray, np.ndarray]) -> np.ndarray:
        """Converts moves from origins-destins-array tuple to array format
        
        If n options are possible the returned array will be of shape (n,2,2) (or (n,4,2) when doubles are rolled)
        
        Parameters
        ----------
        arrMoves : tuple[ndarray, ndarray]
            Tuple of size 2 with two array of shape (26,)
            The first array contains <0 in the locations from where pieces are taken -> origins
            The second array contains >0 in the locations to where pieces are put -> destins
            The rest of the array has to be equal to 0
        
        Returns
        -------
        ndarray
            Array of shape (n,2,2) (or (n,4,2) when doubles are rolled) containign the moves.
            Where n is the number of possible move combinations
            Format: [[[from_0, to_0],
                      [from_1, to_1],
                     ([from_2, to_2],
                      [from_3, to_3])]]
        """
        # Create temp variables
        origins = []; destins = []
        # Find the origin and destins
        for i in range(len(arrMoves[0])):
            # Origins are negative
            if arrMoves[0][i] < 0:
                origins.append(i)
            # Destins are positive
            if arrMoves[1][i] > 0:
                destins.append(i)
        # Check number of moves. Must be either 2 or 4
        if len(origins) not in [2,4] or len(destins) not in [2,4]:
            raise ValueError
        # Create return array
        strMoveOptions = []
        # Generate possible moves options
        moveCombs = np.array(np.meshgrid(origins, destins)).T.reshape(-1,2)
        if len(moveCombs) == 4:
            strMoveOptions.append([moveCombs[0],moveCombs[3]])
            strMoveOptions.append([moveCombs[1],moveCombs[2]])
        else:
            strMoveOptions.append([moveCombs[0],moveCombs[5],moveCombs[10],moveCombs[15]])
            strMoveOptions.append([moveCombs[0],moveCombs[5],moveCombs[11],moveCombs[14]])
            strMoveOptions.append([moveCombs[0],moveCombs[6],moveCombs[ 9],moveCombs[15]])
            strMoveOptions.append([moveCombs[0],moveCombs[6],moveCombs[11],moveCombs[13]])
            strMoveOptions.append([moveCombs[0],moveCombs[7],moveCombs[ 9],moveCombs[14]])
            strMoveOptions.append([moveCombs[0],moveCombs[7],moveCombs[10],moveCombs[13]])
            strMoveOptions.append([moveCombs[1],moveCombs[4],moveCombs[10],moveCombs[15]])
            strMoveOptions.append([moveCombs[1],moveCombs[4],moveCombs[11],moveCombs[14]])
            strMoveOptions.append([moveCombs[1],moveCombs[6],moveCombs[ 8],moveCombs[15]])
            strMoveOptions.append([moveCombs[1],moveCombs[6],moveCombs[11],moveCombs[12]])
            strMoveOptions.append([moveCombs[1],moveCombs[7],moveCombs[ 8],moveCombs[14]])
            strMoveOptions.append([moveCombs[1],moveCombs[7],moveCombs[10],moveCombs[12]])
            strMoveOptions.append([moveCombs[2],moveCombs[4],moveCombs[ 9],moveCombs[15]])
            strMoveOptions.append([moveCombs[2],moveCombs[4],moveCombs[11],moveCombs[13]])
            strMoveOptions.append([moveCombs[2],moveCombs[5],moveCombs[ 8],moveCombs[15]])
            strMoveOptions.append([moveCombs[2],moveCombs[5],moveCombs[11],moveCombs[12]])
            strMoveOptions.append([moveCombs[2],moveCombs[7],moveCombs[ 8],moveCombs[13]])
            strMoveOptions.append([moveCombs[2],moveCombs[7],moveCombs[ 9],moveCombs[12]])
            strMoveOptions.append([moveCombs[3],moveCombs[4],moveCombs[ 9],moveCombs[14]])
            strMoveOptions.append([moveCombs[3],moveCombs[4],moveCombs[10],moveCombs[13]])
            strMoveOptions.append([moveCombs[3],moveCombs[5],moveCombs[ 8],moveCombs[14]])
            strMoveOptions.append([moveCombs[3],moveCombs[5],moveCombs[10],moveCombs[12]])
            strMoveOptions.append([moveCombs[3],moveCombs[6],moveCombs[ 8],moveCombs[13]])
            strMoveOptions.append([moveCombs[3],moveCombs[6],moveCombs[ 9],moveCombs[12]])
        # Convert to numpy array
        strMoveOptions = np.array(strMoveOptions)
        #### TODO as log: print('options: ',strMoveOptions)
        # Discard invalid options
        # Create moveStep array
        moveSteps = strMoveOptions[:,:,1] - strMoveOptions[:,:,0]
        # Check that moveStep are lower than or eq. to 6 and diff to 0
        moveStepsRange = np.all(np.logical_and(abs(moveSteps) <= 6, moveSteps != 0), axis=1)
        #### TODO as log: print(moveStepsRange)
        # Check that moveStep have same sign (a player can only move in one direction)
        moveStepsSign = moveSteps > 0
        moveStepsSign = np.all(moveStepsSign, axis=1)
        #### TODO as log: print(moveStepsSign)
        # Select only valid options
        strMoveOptions = strMoveOptions[np.logical_and(moveStepsSign, moveStepsRange)]
        #### TODO as log: print('slected: ', strMoveOptions)
        # Return move options
        return strMoveOptions

class BackgammonRules():
    
    def __init__(self) -> None:
        pass
    
    def checkMoves(self, positions: np.ndarray, arrMoves: np.ndarray, player: int, diceRolls: np.ndarray) -> bool:
        """Get the first valid moves from arrMoves given the positions, player and dice rolled
        
        Parameters
        ----------
        positions : ndarray
            Array of shape (26,) containing the board positions
        arrMoves : ndarray
            Array of shape (n,m,2) containign the possible moves
            Where n is the number of possible move combinations and m is the number of moves
            Format (for n=1 and m=4): [[[from_0, to_0],
                                        [from_1, to_1],
                                        [from_2, to_2],
                                        [from_3, to_3]]]
        player : int
            Player that makes the moves. Either blackPlayer or whitePlayer
        diceRolls : ndarray
            Array of shape (2,) containing the dice rolls
        
        Returns
        -------
        ndarray
            Array of shape (m,2) conatining the first valid move from arrMoves
            Format (for m=4): [[from_0, to_0],
                               [from_1, to_1],
                               [from_2, to_2],
                               [from_3, to_3]]
        """
        for moves in arrMoves:
            # Create movesSteps array
            movesSteps = moves[:,1] - moves[:,0]
            # Repeat diceRolls 2 times if pairs were rolled
            if diceRolls[0] == diceRolls[1]:
                diceRolls = np.repeat(diceRolls, 2)
            # Check that the moves match the dice rolled
            if not np.all(np.isin(abs(movesSteps), diceRolls)):
                logging.debug(f"Moves {moves} don't match the dice rolled {diceRolls}")
                continue
            # Construct testBoard
            testBoard = BackgammonBoard()
            testBoard.setPositions(positions)
            # Check the permutations of the moves
            for perm in multiset_permutations([x for x in range(len(moves))]):
                # Permute the moves
                movesPerm = moves[perm]
                # Check that all single moves are valid
                for i in range(len(movesPerm)):
                    if self.checkSingleMove(testBoard.positions, player, moves[i][0], moves[i][1]):
                        if i+1 == len(moves):
                            logging.debug(f"Moves {moves} are valid")
                            return True
                        testBoard.applySingleMove(player, BackgammonParser().singleMoveToBoardMove(moves[i]))
                    else:
                        break
                            
                        
            print("move not valid")
        return False

    def checkSingleMove(self, positions: np.ndarray, player: int, moveFrom: int, moveTo: int) -> bool:
        # Check boundary conditions
        if player != blackPlayer and player != whitePlayer:
            print("player value invalid: ", player, " Should be: ", blackPlayer, " or ", whitePlayer)
            return False
        if moveTo > 25 or moveFrom < 0:
            print("move boundaries invalid")
            return False
        if abs(moveTo - moveFrom) > 6:
            print("move larger than 6")
            return False
        # Check direction
        if player == blackPlayer and moveFrom > moveTo:
            print("black direction invalid")
            return False
        if player == whitePlayer and moveFrom < moveTo:
            print("white direction invalid")
            return False
        # Check if origin belongs to player
        if np.sign(positions[moveFrom]) != player:
            print("origin doesn't belong to player")
            return False
        # Check if target belongs to player and has 5+
        if np.sign(positions[moveTo]) == player and abs(positions[moveTo]) >= 5:
            print("target belongs to player and has 5+")
            return False
        # Check if target belongs to oponent and has 2+
        if np.sign(positions[moveTo]) != player and abs(positions[moveTo]) >= 2:
            print("target belongs to oponent and has 2+")
            return False
        # Check if moving 'out' is allowed - black
        if player == blackPlayer and moveTo == 25:
            # Check if all pieces are in the last 6 positions
            if np.any(np.sign(positions[:19]) == player):
                return False
        # Check if moving 'out' is allowed - white
        if player == whitePlayer and moveTo == 0:
            # Check if all pieces are in the last 6 positions
            if np.any(np.sign(positions[6:]) == player):
                return False
        
        # The move is valid
        return True

BackgammonGame()