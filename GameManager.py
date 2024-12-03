

class GameManager :

    def __init__(self):
        self.board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        return
    
    def DetermineColumn(self, move):
        if('1' in move):
            return 0
        elif('2' in move):
            return 1
        elif('3' in move):
            return 2
        else:
            return -1
        
    def PlaceMove(self, move, ID):
        boardPlacer = '?'
        if(ID == 1):
            boardPlacer = 'o'
        elif(ID == 2):
            boardPlacer = 'x'

        #Check for valid column
        if(self.DetermineColumn(move) < 0):
            return False

        #Check for valid row, then attempt to place move
        if('A' in move):
            #If spot has already been played on, return false
            if(self.board[0+(self.DetermineColumn(move))] != ' '):
                return False
            #Else, allow the move to be placed on board at that spot
            self.board[0+(self.DetermineColumn(move))] = boardPlacer

        elif('B' in move):
            if(self.board[3+(self.DetermineColumn(move))] != ' '):
                return False
            self.board[3+(self.DetermineColumn(move))] = boardPlacer

        elif('C' in move):
            if(self.board[6+(self.DetermineColumn(move))] != ' '):
                return False
            self.board[6+(self.DetermineColumn(move))] = boardPlacer

        else:
            return False
        
        return True
    
    def CheckForWin(self):
        #Rows
        if((self.board[0] == 'o' and self.board[1] == 'o' and self.board[2] == 'o') or (self.board[0] == 'x' and self.board[1] == 'x' and self.board[2] == 'x')):
            return True
        elif((self.board[3] == 'o' and self.board[4] == 'o' and self.board[5] == 'o') or (self.board[3] == 'x' and self.board[4] == 'x' and self.board[5] == 'x')):
            return True
        elif((self.board[6] == 'o' and self.board[7] == 'o' and self.board[8] == 'o') or (self.board[6] == 'x' and self.board[7] == 'x' and self.board[8] == 'x')):
            return True
        #Columns
        elif((self.board[0] == 'o' and self.board[3] == 'o' and self.board[6] == 'o') or (self.board[0] == 'x' and self.board[3] == 'x' and self.board[6] == 'x')):
            return True
        elif((self.board[1] == 'o' and self.board[4] == 'o' and self.board[7] == 'o') or (self.board[1] == 'x' and self.board[4] == 'x' and self.board[7] == 'x')):
            return True
        elif((self.board[2] == 'o' and self.board[5] == 'o' and self.board[8] == 'o') or (self.board[2] == 'x' and self.board[5] == 'x' and self.board[8] == 'x')):
            return True
        #Diagonals
        elif((self.board[0] == 'o' and self.board[4] == 'o' and self.board[8] == 'o') or (self.board[0] == 'x' and self.board[4] == 'x' and self.board[8] == 'x')):
            return True
        elif((self.board[2] == 'o' and self.board[4] == 'o' and self.board[6] == 'o') or (self.board[2] == 'x' and self.board[4] == 'x' and self.board[6] == 'x')):
            return True
        return False