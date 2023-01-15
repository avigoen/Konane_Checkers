from audioop import minmax
from copy import copy
import game_rules, random
###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000

class Player(object):
    """ This is the player interface that is consumed by the GameManager. """
    def __init__(self, symbol): self.symbol = symbol # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)
    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def getSymbol(self, isMaxPlayer):
        if self.symbol == 'x':
            return 'x' if isMaxPlayer else 'o'
        return 'o' if isMaxPlayer else 'x'

    def h1(self, board):
        return -len(game_rules.getLegalMoves(board, 'o' if self.symbol == 'x' else 'x'))


# This class has been replaced with the code for a deterministic player.
class MinimaxPlayer(Player):
    def __init__(self, symbol, depth): 
        super(MinimaxPlayer, self).__init__(symbol)
        self.depth = depth

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        moves = game_rules.getLegalMoves(board, self.symbol)
        best_move = moves[0]
        best_score = NEG_INF
        for move in moves:
            updated_board = game_rules.makeMove(board, move)
            score = self.minimax(updated_board, self.depth - 1, False)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def minimax(self, board, depth, isMaxPlayer):
        symbol = self.getSymbol(isMaxPlayer)

        legalMoves = game_rules.getLegalMoves(board, symbol)
        if depth == 0 or len(legalMoves) == 0:
            return self.h1(board)

        if isMaxPlayer:
            return self.calculateMiniMax_MaxPlayerScore(legalMoves, depth, board)
        else:
            return self.calculateMiniMax_MinPlayerSCore(legalMoves, depth, board)

    def calculateMiniMax_MaxPlayerScore(self, legalMoves, depth, board):
        game_score = NEG_INF
        for move in legalMoves:
            updated_board = game_rules.makeMove(board, move)
            score = self.minimax(updated_board, depth - 1, False)
            game_score = max(game_score, score)
        return game_score

    def calculateMiniMax_MinPlayerSCore(self, legalMoves, depth, board):
        game_score = POS_INF
        for move in legalMoves:
            updated_board = game_rules.makeMove(board, move)
            score = self.minimax(updated_board, depth - 1, True)
            game_score = min(game_score, score)
        return game_score

# This class has been replaced with the code for a deterministic player.
class AlphaBetaPlayer(Player):
    def __init__(self, symbol, depth): 
        super(AlphaBetaPlayer, self).__init__(symbol)
        self.depth = depth

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)
    def getMove(self, board):
        moves = game_rules.getLegalMoves(board, self.symbol)
        best_move = moves[0]
        best_score = NEG_INF
        for index, move in enumerate(moves):
            updated_board = game_rules.makeMove(board, move)
            score = self.alphabeta(updated_board, self.depth - 1, NEG_INF, POS_INF, False)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def alphabeta(self, board, depth, alpha, beta, isMaxPlayer):
        symbol = self.getSymbol(isMaxPlayer)

        legalMoves = game_rules.getLegalMoves(board, symbol)
        if depth == 0 or len(legalMoves) == 0:
            return self.h1(board)

        if isMaxPlayer:
            return self.calculateAlphaBetaMaxPlayerScore(board, depth, alpha, beta, legalMoves)
        else:
            return self.calculateAlphaBetaMinPlayerScore(board, depth, alpha, beta, legalMoves)

    def calculateAlphaBetaMinPlayerScore(self, board, depth, alpha, beta, legalMoves):
        game_score = POS_INF
        for move in legalMoves:
            updated_board = game_rules.makeMove(board, move)
            score = self.alphabeta(updated_board, depth - 1, alpha, beta, True)
            game_score = min(game_score, score)
            if game_score <= alpha:
                break
            beta = min(beta, game_score)
        return game_score

    def calculateAlphaBetaMaxPlayerScore(self, board, depth, alpha, beta, legalMoves):
        game_score = NEG_INF
        for move in legalMoves:
            updated_board = game_rules.makeMove(board, move)
            score = self.alphabeta(updated_board, depth - 1, alpha, beta, False)
            game_score = max(game_score, score)
            if game_score >= beta:
                break
            alpha = max(alpha, game_score)
        return game_score


class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return random.choice(legalMoves)
        else: return None


class DeterministicPlayer(Player):
    def __init__(self, symbol): super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)
    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedException('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)

def nodeHeuristic(board, symbol):
    board_corners = list(game_rules.getCorners(board))
    corners_have_symbol = sum([int(corner == symbol) for corner in board_corners])
    score = len(game_rules.getLegalMoves(board, symbol)) - len(game_rules.getLegalMoves(board, 'o' if symbol == 'x' else 'x')) + corners_have_symbol
    return score