import copy
import time

import PySimpleGUI as sg

from PyAgrippa.Boards.Board import IBoard
from PyAgrippa.Boards.SCPSBoard import BoardSCPS
from PyAgrippa.GUI.GUILayout import IGUILayout, DefaultGUILayout
from PyAgrippa.Squares.Square import ISquare


class BoardRenderer:
    """
    Provides functionality to render a board (with of course the pieces and squares on it as well). Also provides
    functionality to play a game against the chess engine Agrippa. However, the focus remains on visualization and not
    control, i.e. it's not meant to tweak machine parameters but it IS meant to e.g. show the board state, machine
    evaluation, ...
    """

    def __init__(self, layout: IGUILayout = DefaultGUILayout(),
                 initialBoard: IBoard = None):
        self.layout = layout
        self.board = initialBoard
        self.window = None

    def changeLayout(self, newLayout: IGUILayout):
        raise NotImplementedError

    def renderSquare(self, square: ISquare):
        if square.isLightSquare():
            color = self.layout.getLightSquareColor()
        else:
            color = self.layout.getDarkSquareColor()
        piece = self.board.getPieceOn(square)
        if piece is not None:
            image = piece.getImage(layout=self.layout)
        else:
            image = self.layout.getBlankImage()
        return sg.RButton('', image_filename=image, size=(1, 1), button_color=('white', color), pad=(0, 0), key=square)

    def updateSquare(self, square: ISquare):
        if square.isLightSquare():
            color = self.layout.getLightSquareColor()
        else:
            color = self.layout.getDarkSquareColor()
        piece = self.board.getPieceOn(square)
        if piece is not None:
            image = piece.getImage(layout=self.layout)
        else:
            image = self.layout.getBlankImage()
        button = self.window[square]
        button.Update(button_color=('white', color), image_filename=image)
        # return sg.RButton('', image_filename=image, size=(1, 1), button_color=('white', color), pad=(0, 0), key=square)

    def start(self):
        """
        Initializes the main window and loads the board.
        """
        menu_def = [['&File', ['E&xit']],
                    ['&Layout', '&About'], ]

        # sg.SetOptions(margins=(0,0))
        sg.ChangeLookAndFeel(self.layout.getSGLookAndFeel())
        # the main board display layout
        boardLayout = []
        rankLabels = self.layout.getRankLabels()

        # loop though squares and create buttons with images
        for j, rank in reversed(list(enumerate(self.board.getSquares()))):
            row = []
            for square in rank:
                i = square.getFile()
                j = square.getRank()
                row.append(self.renderSquare(square))
            row.append(sg.T(self.layout.getFileLabels()[j] + '   ', font=self.layout.getFileLabelFont()))
            boardLayout.append(row)
        # add the labels across bottom of board
        if rankLabels is not None:
            boardLayout.append(
                # [sg.T(' ')] +
                [sg.T('{}'.format(label), pad=((23, 27), 0), font=self.layout.getRankLabelFont())
                 for label in rankLabels]
            )

        # setup the controls on the right side of screen
        boardControls = [[sg.RButton('Play', )],
                         [sg.RButton('Load')],
                         ]

        # the main window layout
        layout = [[sg.Menu(menu_def, tearoff=False)],
                  [sg.Column(boardLayout),
                   sg.Column(boardControls)]]

        self.window = sg.Window('Agrippa Chess', default_button_element_size=(12, 1), auto_size_buttons=False,
                                # size=(900, 750)
                                ).Layout(layout)

    def refresh(self):
        # #  pySimpleGUI does not allow dynamic boards, so I'm gonna follow the author's advice and remove the window
        # oldWindow = self.window
        # self.start()
        # self.show()
        # # time.sleep(0.5)
        # oldWindow.close()
        for j, rank in reversed(list(enumerate(self.board.getSquares()))):
            for square in rank:
                self.updateSquare(square)
        self.show()

    def show(self):
        """
        Control is transferred to the user for 0 seconds.
        """
        _ = self.window.Read(timeout=0., timeout_key=None)

    def waitForUserExit(self):
        while True:
            button, value = self.window.Read()
            if button in (None, 'Exit'):
                break
        # if button == 'About...':
        #     sg.Popup('GUI for the PyAgrippa chess program developed by Tom De Weer.')
        # if type(button) is tuple and moves is not None and i < len(moves):
        #     move = moves[i]  # get the current move
        #     self.window.FindElement('_movelist_').Update(value='{}   {}\n'.format(i + 1, str(move)), append=True)
        #     move_from = move.from_square  # parse the move-from and move-to squares
        #     move_to = move.to_square
        #     row, col = move_from // 8, move_from % 8
        #     piece = board[row][col]  # get the move-from piece
        #     button = window.FindElement(key=(row, col))
        #     for x in range(3):
        #         button.Update(button_color=('white', 'red' if x % 2 else 'white'))
        #         self.window.Refresh()
        #         time.sleep(.05)
        #     board[row][col] = BLANK  # place blank where piece was
        #     row, col = move_to // 8, move_to % 8  # compute move-to square
        #     board[row][col] = piece  # place piece in the move-to square
        #     redraw_board(self.window, board)
        #     i += 1

    def playGame(self):
        raise NotImplementedError
