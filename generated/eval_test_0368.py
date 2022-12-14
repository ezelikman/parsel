# chess_game takes a board and returns the winner of the game.
def chess_game(board):
    if weight(board) == 0:
        return 'Draw'
    if weight(board) > 0:
        return 'White'
    if weight(board) < 0:
        return 'Black'

# weight takes a board and returns the weight of the board.
def weight(board):
	weight = 0
	for row in range(len(board)):
		for col in range(len(board[row])):
			if board[row][col] != '.':
				weight += weight_helper(board, row, col, 0)
	return weight

# weight_helper takes a board, a row, a column, and a weight and returns the weight of the board.
def weight_helper(board, row, col, weight):
    if board[row][col] == '.':
        return 0
    elif board[row][col] == 'Q':
        return weight + 9
    elif board[row][col] == 'R':
        return weight + 5
    elif board[row][col] == 'B':
        return weight + 3
    elif board[row][col] == 'N':
        return weight + 3
    elif board[row][col] == 'P':
        return weight + 1
    elif board[row][col] == 'q':
        return weight - 9
    elif board[row][col] == 'r':
        return weight - 5
    elif board[row][col] == 'b':
        return weight - 3
    elif board[row][col] == 'n':
        return weight - 3
    elif board[row][col] == 'p':
        return weight - 1
    else:
        return weight


assert repr(str(chess_game('...QK...\n........\n........\n........\n........\n........\n........\n...rk...'))) == repr('White')
assert repr(str(chess_game('rnbqkbnr\npppppppp\n........\n........\n........\n........\nPPPPPPPP\nRNBQKBNR'))) == repr('Draw')
assert repr(str(chess_game('rppppppr\n...k....\n........\n........\n........\n........\nK...Q...\n........'))) == repr('Black')
assert repr(str(chess_game('....bQ.K\n.B......\n.....P..\n........\n........\n........\n...N.P..\n.....R..'))) == repr('White')
assert repr(str(chess_game('b....p..\nR.......\n.pP...b.\npp......\nq.PPNpPR\n..K..rNn\nP.....p.\n...Q..B.'))) == repr('White')
assert repr(str(chess_game('...Nn...\n........\n........\n........\n.R....b.\n........\n........\n......p.'))) == repr('White')
assert repr(str(chess_game('...p..Kn\n.....Pq.\n.R.rN...\n...b.PPr\np....p.P\n...B....\np.b.....\n..N.....'))) == repr('Black')
assert repr(str(chess_game('q.......\nPPPPPPPP\n........\n........\n........\n........\n........\n........'))) == repr('Black')
assert repr(str(chess_game('q.......\nPPPPPPPP\nP.......\n........\n........\n........\n........\n........'))) == repr('Draw')
assert repr(str(chess_game('q.......\nPPPPPPPP\nPP......\n........\n........\n........\n........\n........'))) == repr('White')
assert repr(str(chess_game('r.......\nPPPP....\n........\n........\n........\n........\n........\n........'))) == repr('Black')
assert repr(str(chess_game('r.......\nPPPPP...\n........\n........\n........\n........\n........\n........'))) == repr('Draw')
assert repr(str(chess_game('r.......\nPPPPPP..\n........\n........\n........\n........\n........\n........'))) == repr('White')
assert repr(str(chess_game('b.......\nPP......\n........\n........\n........\n........\n........\n........'))) == repr('Black')
assert repr(str(chess_game('b.......\nPPP.....\n........\n........\n........\n........\n........\n........'))) == repr('Draw')
assert repr(str(chess_game('b.......\nPPPP....\n........\n........\n........\n........\n........\n........'))) == repr('White')
assert repr(str(chess_game('n.......\nPP......\n........\n........\n........\n........\n........\n........'))) == repr('Black')
assert repr(str(chess_game('n.......\nPPP.....\n........\n........\n........\n........\n........\n........'))) == repr('Draw')
assert repr(str(chess_game('n.......\nPPPP....\n........\n........\n........\n........\n........\n........'))) == repr('White')
assert repr(str(chess_game('Q.......\npppppppp\n........\n........\n........\n........\n........\n........'))) == repr('White')
assert repr(str(chess_game('Q.......\npppppppp\np.......\n........\n........\n........\n........\n........'))) == repr('Draw')
assert repr(str(chess_game('Q.......\npppppppp\npp......\n........\n........\n........\n........\n........'))) == repr('Black')
assert repr(str(chess_game('R.......\npppp....\n........\n........\n........\n........\n........\n........'))) == repr('White')
assert repr(str(chess_game('R.......\nppppp...\n........\n........\n........\n........\n........\n........'))) == repr('Draw')
assert repr(str(chess_game('R.......\npppppp..\n........\n........\n........\n........\n........\n........'))) == repr('Black')
assert repr(str(chess_game('B.......\npp......\n........\n........\n........\n........\n........\n........'))) == repr('White')
assert repr(str(chess_game('B.......\nppp.....\n........\n........\n........\n........\n........\n........'))) == repr('Draw')
assert repr(str(chess_game('B.......\npppp....\n........\n........\n........\n........\n........\n........'))) == repr('Black')
assert repr(str(chess_game('N.......\npp......\n........\n........\n........\n........\n........\n........'))) == repr('White')
assert repr(str(chess_game('N.......\nppp.....\n........\n........\n........\n........\n........\n........'))) == repr('Draw')
assert repr(str(chess_game('N.......\npppp....\n........\n........\n........\n........\n........\n........'))) == repr('Black')
assert repr(str(chess_game('qqqqqqqq\nqqqqqqqq\nqqqqqqqq\nqqqqqqqq\nqqqqqqqq\nqqqqqqqq\nqqqqqqqq\nqqqqqqqq'))) == repr('Black')
assert repr(str(chess_game('QQQQQQQQ\nQQQQQQQQ\nQQQQQQQQ\nQQQQQQQQ\nQQQQQQQQ\nQQQQQQQQ\nQQQQQQQQ\nQQQQQQQQ'))) == repr('White')
assert repr(str(chess_game('qqqqqqqq\nqqqqqqqq\nqqqqqqqq\nqqqqqqqq\nQQQQQQQQ\nQQQQQQQQ\nQQQQQQQQ\nQQQQQQQQ'))) == repr('Draw')
assert repr(str(chess_game('..KQBN..\n........\n........\n....q...\n..p.....\n....k...\n........\n........'))) == repr('White')
assert repr(str(chess_game('..K....Q\n........\n....q...\n........\n........\n........\n........\n........'))) == repr('Draw')
assert repr(str(chess_game('KKKKKKK.\n........\n........\n........\n........\n........\n........\nq.......'))) == repr('Black')
assert repr(str(chess_game('QQQQQQQQ\nQQQQQQQQ\n........\n........\n........\n........\nrrrrrr..\nrrrrrrrr'))) == repr('White')
assert repr(str(chess_game('........\n........\n........\n........\n........\n........\n........\n........'))) == repr('Draw')
assert repr(str(chess_game('P.......\n........\n........\n........\n........\n........\n........\n........'))) == repr('White')
assert repr(str(chess_game('...b....\n...np...\n........\n........\n........\n...N....\n...B....\n...R....'))) == repr('White')
assert repr(str(chess_game('........\n........\n........\n........\n........\n........\nNN......\n........'))) == repr('White')
assert repr(str(chess_game('........\n........\n........\n........\n........\n........\n........\n.......n'))) == repr('Black')
assert repr(str(chess_game('n.......\nn.......\nn.......\nn.......\nn.......\nn.......\nn.......\nn.......'))) == repr('Black')
assert repr(str(chess_game('NNNNNNNN\nNNNNNNNN\nNNNNNNNN\nNNNNNNNN\nNNNNNNNN\nNNNNNNNN\nKk......\nq.......'))) == repr('White')
assert repr(str(chess_game('........\nNN......\n........\n........\n........\n........\n........\n........'))) == repr('White')
assert repr(str(chess_game('K.......\n........\n........\n........\n........\n........\n........\n........'))) == repr('Draw')
assert repr(str(chess_game('Q.......\nkkk.....\n........\n........\n........\n........\n........\n........'))) == repr('White')
assert repr(str(chess_game('Kn......\n........\n........\n........\n........\n........\n........\n........'))) == repr('Black')
assert repr(str(chess_game('........\n........\n........\n........\n........\n........\n........\nn.......'))) == repr('Black')
assert repr(str(chess_game('KKKKKKKK\npppppppp\n........\n........\n........\n........\n........\n........'))) == repr('Black')
assert repr(str(chess_game('........\n...b....\n........\n........\n........\n........\n........\n.......K'))) == repr('Black')
assert repr(str(chess_game('........\n........\n........\n........\n........\n........\n........\n......Kp'))) == repr('Black')
assert repr(str(chess_game('........\n........\n........\n........\n........\n........\n........\n.......Q'))) == repr('White')
assert repr(str(chess_game('........\n........\n........\n........\n........\n........\n........\n......Bp'))) == repr('White')


