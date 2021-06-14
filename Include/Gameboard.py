import copy, re

class Gameboard:
    def __init__(self):
        #Construct blocks
        self.white_win = False
        self.black_win = False
        self.winUtility = 1000
        self.loseUtility = -1000
        self.win = False
        self.tie = False
        self.moves = []
        self.firstPlayerTurn = True
        self.blocks = []
        for i in range(4):
            positions = [None]*9
            self.blocks.append(positions)

    def makeMove(self,moveString):
        success = None
        if self.firstPlayerTurn:
            success = self.interpert_and_doMove(moveString,"w")
        else:
            success = self.interpert_and_doMove(moveString, "b")

        if(success):
            self.firstPlayerTurn = not self.firstPlayerTurn
        return success

    def interpert_and_doMove(self,moveString,piece):
        params = re.split(' |/',moveString)

        valid = self.put(piece,int(params[0])-1,int(params[1])-1)
        if(valid):
            self.moves.append(moveString)
            if(not self.win):
                self.rotate(int(params[2][0])-1,params[2][1])

        return valid

    def put(self,value,block,position):
        if(self.blocks[block][position] == None):
            self.blocks[block][position] = value
        else:
            print("Invalid Move!")
            return False

        w_util, b_util = self.utility_all()
        if (w_util == self.winUtility):
            self.white_win = True
        if(b_util == self.loseUtility):
            self.black_win = True
        if(self.white_win and self.black_win):
            self.tie = True
        elif(self.white_win or self.black_win):
            self.win = True

        return True

    def get(self,block,position):
        return self.blocks[block][position]

    def rotate(self,block,direction):

        # helper method to convert 2D matrix coordinates into 1D array position
        # makes writing the rotation easier
        def convert(row,col):
            return row*3 + col

        temp = [None] * 9
        for row in range(3):
            for col in range(3):
                if(direction == "L"):
                    temp[convert(2 - col, row)] = self.blocks[block][convert(row, col)]
                else:
                    temp[convert(col, 2 - row)] = self.blocks[block][convert(row, col)]

        self.blocks[block] = temp

        w_util, b_util = self.utility_all()
        if (w_util == self.winUtility):
            self.white_win = True
        if (b_util == self.loseUtility):
            self.black_win = True
        if (self.white_win and self.black_win):
            self.tie = True
        elif (self.white_win or self.black_win):
            self.win = True


    def combined_utility(self):
        w_util, b_util = self.utility_all()
        return w_util + b_util;

    def utility(self):
        w_util, b_util = self.utility_all()
        return w_util if self.firstPlayerTurn else b_util
    def utility_all(self):



        #helper method to convert 2D matrix coordinates into block and position
        def outer_convert(row,col):
            #helper method to convert 2D matrix coordinates into 1D array position
            def inner_convert(row,col):
                return row*3 + col

            pos = inner_convert(row%3,col%3)
            block = 2*int(row/3) + int(col/3)

            return block, pos



        max_consecutive_w = 0;
        max_consecutive_b = 0;

        w_middle = 0
        b_middle = 0

        # count horizontal
        for r in range(6):
            w_count = 0
            b_count = 0
            for c in range(6):
                block, pos = outer_convert(r,c)
                if(self.blocks[block][pos] == "w"):
                    if((r==1 or r==4) and (c==1 or c==4)):
                        w_middle += 1

                    w_count += 1
                    b_count = 0
                elif(self.blocks[block][pos] == "b"):
                    if ((r == 1 or r == 4) and (c == 1 or c == 4)):
                        b_middle += 1

                    b_count += 1
                    w_count = 0
                else:
                    w_count = 0
                    b_count = 0

                max_consecutive_w = max(max_consecutive_w, w_count)
                max_consecutive_b = max(max_consecutive_b, b_count)

        #count vertical
        for c in range(6):
            w_count = 0
            b_count = 0
            for r in range(6):
                block, pos = outer_convert(r,c)
                if(self.blocks[block][pos] == "w"):
                    w_count += 1
                    b_count = 0
                elif(self.blocks[block][pos] == "b"):
                    b_count += 1
                    w_count = 0
                else:
                    w_count = 0
                    b_count = 0

                max_consecutive_w = max(max_consecutive_w, w_count)
                max_consecutive_b = max(max_consecutive_b, b_count)

        #count diagonals
        #topleft to bottomright
        for d in range(2):
            for i in range(6):
                w_count = 0
                b_count = 0
                for j in range(6-i):
                    block, pos = outer_convert(j+i,j) if d == 0 else outer_convert(j,j+i)
                    if(self.blocks[block][pos] == "w"):
                        w_count += 1
                        b_count = 0
                    elif(self.blocks[block][pos] == "b"):
                        b_count += 1
                        w_count = 0
                    else:
                        w_count = 0
                        b_count = 0

                    max_consecutive_w = max(max_consecutive_w, w_count)
                    max_consecutive_b = max(max_consecutive_b, b_count)
        #bottomleft to topright
        for d in range(2):
            for i in range(6):
                w_count = 0
                b_count = 0
                for j in range(6 - i):
                    block, pos = outer_convert(5-(j + i), j) if d == 0 else outer_convert(5-j, j + i)
                    if (self.blocks[block][pos] == "w"):
                        w_count += 1
                        b_count = 0
                    elif (self.blocks[block][pos] == "b"):
                        b_count += 1
                        w_count = 0
                    else:
                        w_count = 0
                        b_count = 0

                    max_consecutive_w = max(max_consecutive_w, w_count)
                    max_consecutive_b = max(max_consecutive_b, b_count)

        #return logic

        # returns tuple: (w utility, b utility)
        return max_consecutive_w*5 +w_middle if (max_consecutive_w < 5) else self.winUtility, \
               -max_consecutive_b*5 -b_middle if (max_consecutive_b < 5) else self.loseUtility

    def potentialMoves(self):
        potentialMoves = []
        for block in range(4):
            for pos in range(9):
                for rblock in range(4):
                    if(self.blocks[block][pos] == None):
                        potentialMoves.append(str(block + 1) + "/" + str(pos + 1) + " " + str(rblock + 1) + "L")
                        potentialMoves.append(str(block + 1) + "/" + str(pos + 1) + " " + str(rblock + 1) + "R")

        return potentialMoves

    def __str__(self):
        bar = "+-------+-------+\n"
        out = [bar]
        for block in range(2,5,2):
            for i in range(0,7,3):
                for j in range(block-2,block):
                    out.append("| ")
                    for k in range(3):
                        val = self.get(j,i+k)
                        out.append(val+ " ") if val != None else out.append(". ")

                out.append("|\n")

            out.append(bar)
        return ''.join(out)


    def copy(self):
        return copy.deepcopy(self)