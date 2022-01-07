import time

from PyAgrippa.Boards.SCPSBoard import BoardSCPS

if __name__ == '__main__':

    board = BoardSCPS()
    board.setInitialSetup()

    N = 100000
    tic = time.time()
    for i in range(N):
        # pyboard = board.toPythonChessBoard()
        hash(board)
    toc = time.time()
    total = toc - tic
    print(total)
    print(total / N)
