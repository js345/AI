class search:



    #todo
    def startSearch(self, evaluation, stradegy, depth, board, player):
        heu = self.heuristic(board,player,evaluation)


        return board


    def heuristic(self, board, player, evaluation):
        own = 0;
        oppo = 0;
        '''
        for(i: board):
            if(i == player):
                own += 1
            else:
                oppo += 1
        if(evaluation == 0): #defensive
            return 2*own+ random
        else return 2*(30-oppo) + random
        '''


    def search(self, stradegy,heur, player, depth, board):
        if stradegy == 0:   # minimax
            a = 0
        else:               #alpha beta
            return
