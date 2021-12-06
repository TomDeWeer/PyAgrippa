from PyAgrippa.Boards.Board import BoardSCPS
from PyAgrippa.GUI.BoardRenderer import BoardRenderer

renderer = BoardRenderer(initialBoard=BoardSCPS.initialSetup())
renderer.start()
renderer.showAndWaitForUserInput()
