from Boards.Board import BoardSCPS
from GUI.BoardRenderer import BoardRenderer

renderer = BoardRenderer(initialBoard=BoardSCPS.initialSetup())
renderer.start()
renderer.showAndWaitForUserInput()
