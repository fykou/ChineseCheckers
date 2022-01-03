import numpy as np


class Board:
    class Selection:
        def __init__(self, board):
            self.board = board
            self.coord = None
            self.legalMoves = None
            self.value = None
            self.selected = False

        def select(self, coord):
            if not self.selected:
                self.coord = coord
                self.value = self.board.array[coord] # save value of piece
                self.board.array[coord] = 10 # highlight selected piece
                self.legalMoves = self.board.findLegalMoves(coord, validMoves = []) # find legal moves
                for move in self.legalMoves:
                    self.board.array[move] = 11 # highlight legal moves
                self.selected = True
            else:
                raise Exception(
                    "Error - A piece already selected at ", self.coord)

        def deselect(self):
            if self.selected:
                self.board.array[self.coord] = self.value # restore value of piece
                for move in self.legalMoves:
                    self.board.array[move] = 0 # remove highlighted legal moves
                self.coord = None
                self.legalMoves = None # reset legal moves
                self.value = None
                self.selected = False
            else:
                raise Exception("Error - No piece selected")

        def postMove(self, coord):
            if self.selected:
                self.board.array[self.coord[0]][self.coord[1]] = 0
                for move in self.legalMoves:
                    self.board.array[move] = 0
                self.board.array[coord[0]][coord[1]] = self.value
                self.coord = None
                self.legalMoves = None
                self.value = None
                self.selected = False
            else:
                raise Exception("Error - No piece selected")

    def __init__(self):

        self.selection = self.Selection(self)

        self.array = np.zeros((17, 25), dtype=int)

        self.array[:][:] = -1

        initBoard = dict()

        initBoard["board"] =  (0, [[4, 8], [4, 10], [4, 12], [4, 14], [4, 16], [5, 7], [5, 9], [5, 11], [5, 13], [5, 15], [5, 17], [6, 6], [6, 8], [6, 10], [6, 12], [6, 14], [6, 16], [6, 18], [7, 5], [7, 7], [7, 9], [7, 11], [7, 13], [7, 15], [7, 17], [7, 19], [7, 5], [7, 7], [7, 9], [7, 11], [7, 13], [7, 15], [7, 17], [7, 19], [8, 4], [8, 6], [8, 8], [8, 10], [8, 12], [8, 14], [8, 16], [8, 18], [8, 20], [9, 5], [9, 7], [9, 9], [9, 11], [9, 13], [9, 15], [9, 17], [9, 19], [10, 6], [10, 8], [10, 10], [10, 12], [10, 14], [10, 16], [10, 18], [11, 7], [11, 9], [11, 11], [11, 13], [11, 15], [11, 17], [12, 8], [12, 10], [12, 12], [12, 14], [12, 16]])
        initBoard["player1"] = (1, [[0, 12], [1, 11], [1, 13], [2, 10], [2, 12], [2, 14], [3, 9], [3, 11], [3, 13], [3, 15]])
        initBoard["player2"] = (2, [[4, 18], [4, 20], [4, 22], [4, 24], [5, 19], [5, 21], [5, 23], [6, 20], [6, 22], [7, 21]])
        initBoard["player3"] = (3, [[9, 21], [10, 20], [10, 22], [11, 19], [11, 21], [11, 23], [12, 18], [12, 20], [12, 22], [12, 24]])
        initBoard["player4"] = (4, [[13, 9], [13, 11], [13, 13], [13, 15], [14, 10], [14, 12], [14, 14], [15, 11], [15, 13], [16, 12]])
        initBoard["player5"] = (5, [[9, 3], [10, 2], [10, 4], [11, 1], [11, 3], [11, 5], [12, 0], [12, 2], [12, 4], [12, 6]])
        initBoard["player6"] = (6, [[4, 0], [4, 2], [4, 4], [4, 6], [5, 1], [5, 3], [5, 5], [6, 2], [6, 4], [7, 3]])

        for playerPositions in initBoard.values():
            for position in playerPositions[1]:
                self.array[position[0]][position[1]] = playerPositions[0]

    def findNeighbors(self, piece):
        adjacent = dict()
        adjacent["right"] = (piece[0], piece[1] + 2)  # right
        adjacent["left"] = (piece[0], piece[1] - 2)  # left
        adjacent["upLeft"] = (piece[0] - 1, piece[1] - 1)  # up left
        adjacent["upRight"] = (piece[0] - 1, piece[1] + 1)  # up right
        adjacent["downLeft"] = (piece[0] + 1, piece[1] - 1)  # down left
        adjacent["downRight"] = (piece[0] + 1, piece[1] + 1)  # down right
        return adjacent


    def findLegalMoves(self, piece, validMoves, depth = 0, queue=[]):
        if piece not in validMoves:
            
            # for all neighbors
            for neighborPosition in self.findNeighbors(piece).values():

                # check out of bounds
                try:
                    self.array[neighborPosition]
                except IndexError:
                    continue

                # add single moves from origin
                if depth == 0 and self.array[neighborPosition] == 0 and neighborPosition not in validMoves:
                    validMoves.append(neighborPosition)

                # if neighbor is contains piece, check if jump is possible
                if self.array[neighborPosition] > 0:
                    newLocation = (neighborPosition[0] + (neighborPosition[0] - piece[0]), neighborPosition[1] + (neighborPosition[1] - piece[1]))

                    # check if newlocation is out of bounds and is empty
                    try:
                        self.array[newLocation]
                        if self.array[newLocation] == 0 and newLocation not in queue and newLocation not in validMoves:
                            queue.append(newLocation)
                    except IndexError:
                        continue

            validMoves.append(piece)
        
        # check if there is more nodes to explore
        if len(queue) > 0:
            piece = queue.pop(0)
            if not piece in validMoves:
                validMoves = self.findLegalMoves(piece, validMoves, depth + 1, queue)

        if self.selection.coord in validMoves:
            validMoves.remove(self.selection.coord)

        return validMoves

    def movePiece(self, toCoord):
        if toCoord in self.selection.legalMoves:
            self.selection.postMove(toCoord)
            return True
        else:
            return False

    def selectPiece(self, coord):
        if self.array[coord[0]][coord[1]] != 0:
            self.selection.select(coord)
        else:
            raise Exception("Error - No piece selected")

    def deselectPiece(self):
        self.selection.deselect()
