import random

class AI:
    #type = 0 for minmax, type = 1 for alpha-beta purning
    def __init__(self,type = 0):
        self.algorithm = None
        self.visited = dict()
        self.nodesExpanded = 0
        self.depthExpanded = 0
        if(type == -1):
            self.algorithm = self.random_choice
        elif(type == 0):
            self.algorithm = self.min_max
        else:
            self.algorithm = self.alpha_beta

    def random_choice(self,board,maxdepth):
        options = board.potentialMoves()
        return options[random.randint(0,len(options)-1)]
    def min_max(self,board,maxdepth,depth=0):
        chosenMove = [None]
        def min_max_helper(AI,board,maxdpeth,depth,chosenMove):
            AI.depthExpanded = max(AI.depthExpanded,depth)
            if(depth>=maxdepth):
                return board.combined_utility()
            elif (board.utility() == board.winUtility):
                return board.winUtility
            elif (board.utility() == board.loseUtility):
                return board.loseUtility
            else:
                options = board.potentialMoves()
                bestMove = None
                bestUtility = None
                for move in options:
                    next = board.copy()
                    next.makeMove(move)
                    if(str(next.blocks) in AI.visited):
                        nextUtility = AI.visited[str(next.blocks)]
                    else:
                        nextUtility = min_max_helper(AI,next,maxdepth,depth+1,chosenMove)
                        AI.visited[str(next.blocks)] = nextUtility

                    AI.nodesExpanded += 1
                    if(bestMove == None):
                        bestMove = move
                        bestUtility = nextUtility

                    if (bestUtility < nextUtility if board.firstPlayerTurn else bestUtility > nextUtility):
                        bestMove = move
                        bestUtility = nextUtility

                chosenMove[0] = bestMove
                return int(bestUtility)

        min_max_helper(self,board,maxdepth,depth,chosenMove)
        return chosenMove[0]

    def alpha_beta(self,board,maxdepth,depth=0):
        chosenMove = [None]
        def alpha_beta_helper(AI,board,maxdpeth,depth,alpha,beta,chosenMove):
            AI.depthExpanded = max(AI.depthExpanded,depth)
            if(depth>=maxdepth):
                return board.combined_utility()
            elif (board.utility() == board.winUtility):
                return board.winUtility
            elif (board.utility() == board.loseUtility):
                return board.loseUtility
            else:
                #options = AI.preprocess(board,board.potentialMoves()) #the sorting time for pre-processing reduces performance more than it improves it
                options = board.potentialMoves() #No pre-processing
                bestMove = None
                bestUtility = None
                for move in options:
                    next = board.copy()
                    next.makeMove(move)
                    if(str(next.blocks) in AI.visited):
                        nextUtility = AI.visited[str(next.blocks)]
                    else:
                        nextUtility = alpha_beta_helper(AI,next,maxdepth,depth+1,alpha,beta,chosenMove)
                        AI.visited[str(next.blocks)] = nextUtility

                    AI.nodesExpanded += 1
                    if(bestMove == None):
                        bestMove = move
                        bestUtility = nextUtility

                    if (bestUtility < nextUtility if board.firstPlayerTurn else bestUtility > nextUtility):
                        bestMove = move
                        bestUtility = nextUtility

                    if (board.firstPlayerTurn):
                        alpha = max(alpha, int(nextUtility))
                    else:
                        beta = min(beta, int(nextUtility))

                    if beta <= alpha:
                        break;

                chosenMove[0] = bestMove
                return int(bestUtility)

        alpha_beta_helper(self,board,maxdepth,depth,float("-inf"),float("inf"),chosenMove)
        return chosenMove[0]

    def preprocess(self,board,options):

        def utilities(move):
            duplicate = board.copy()
            duplicate.makeMove(move)
            return duplicate.combined_utility()

        options.sort(key=utilities, reverse = True)
        return options

    def makeMove(self,board,maxdepth = 2):
        w_util, b_util = board.utility_all()
        self.nodesExpanded = 0
        self.depthExpanded = 0
        move = self.algorithm(board,maxdepth)
        board.makeMove(move)
        print("Nodes expanded:",self.nodesExpanded)
        print("Max Depth:", self.depthExpanded)
        self.visited.clear()
        return move

    def all_utilities(self,board, moves):
        utilities = []
        for move in moves:
            newBoard = board.copy()
            newBoard.makeMove(move)
            utilities.append(newBoard.utility())

        return utilities