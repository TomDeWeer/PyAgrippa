from Boards.Board import BoardSquareCenteredWithPieceSets
from GUI.BoardRenderer import BoardRenderer

renderer = BoardRenderer(initialBoard=BoardSquareCenteredWithPieceSets.initialSetup())
renderer.start()
renderer.showAndWaitForUserInput()
