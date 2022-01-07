import time

from PyAgrippa.Boards.SCPSBoard import BoardSCPS
from PyAgrippa.GUI.BoardRenderer import BoardRenderer

board = BoardSCPS()
board.setInitialSetup()
renderer = BoardRenderer(initialBoard=board)
renderer.start()
print('Showing...')
renderer.show()
time.sleep(2.)
print('Control returned to python. ')
print('Applying e4.')
board.movePieceSC(start=board.getSquareViaStr('e2'), end=board.getSquareViaStr('e4'))
print('Refreshing board...')
renderer.refresh()
time.sleep(2.)
print('Applying e5.')
board.movePieceSC(start=board.getSquareViaStr('e7'), end=board.getSquareViaStr('e5'))
renderer.refresh()
print('Now waiting for user to exit GUI.')
renderer.waitForUserExit()
