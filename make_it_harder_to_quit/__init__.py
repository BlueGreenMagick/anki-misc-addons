from aqt import AnkiQt, mw
from anki.hooks import wrap

from aqt.qt import *
from aqt.utils import tooltip

MSG = """Are you sure you want to quit Anki?
You still have some reviews left.
"""
ADDON_closeui = None
UI_on = False
close_enabled = False


class UI(QWidget):

    def __init__(self):
        super(UI, self).__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.timer = 11
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.qtimer = None
        self.setup_ui()

    def closeEvent(self, evt):
        global UI_on
        UI_on = False
        evt.accept()

    def onCancel(self):
        self.close()

    def onQuit(self):
        global close_enabled
        close_enabled = True
        mw.close()
        self.close()

    def timerfunc(self):
        if self.timer > 0:
            self.timer -= 1
            self.timerLabel.setText(str(self.timer))
        else:
            self.qtimer.stop()
            self.quitButton.setEnabled(True)

    def setup_ui(self):
        mainLayout = QVBoxLayout()
        self.setLayout(mainLayout)

        mainLabel = QLabel(MSG)
        timerLabel = QLabel("")
        self.timerLabel = timerLabel

        mainLayout.addWidget(mainLabel)
        mainLayout.addWidget(timerLabel)

        quitButton = QPushButton("Quit")
        quitButton.setDisabled(True)
        quitButton.clicked.connect(self.onQuit)
        self.quitButton = quitButton
        cancelButton = QPushButton("Go Back")
        cancelButton.setDefault(True)
        cancelButton.setShortcut("Return")
        cancelButton.clicked.connect(self.onCancel)

        btnLayout = QHBoxLayout()
        btnLayout.addStretch(1)
        btnLayout.addWidget(cancelButton)
        btnLayout.addWidget(quitButton)
        mainLayout.addLayout(btnLayout)

        self.setWindowTitle('Quit?')
        self.qtimer = QTimer(self)
        self.qtimer.timeout.connect(self.timerfunc)
        self.qtimer.start(1000)

        self.move(QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())

        self.show()
        self.setFocus()

def check_if_not_done():
    # from aqt.deckbrowser.DeckBrowser._renderStats
    nameMap = mw.col.decks.nameMap()
    dueTree = mw.col.sched.deckDueTree()
    for node in dueTree:
        name, did, due, lrn, new, children = node
        if "::" in mw.col.decks.get(did):
            continue
        if due + lrn:
            return 1

    return 0

def onClose(self, evt, _old):
    global ADDON_closeui
    global UI_on
    if not close_enabled and check_if_not_done():
        evt.ignore()
        if not UI_on:
            UI_on = True
            ADDON_closeui = UI()
    else:
        _old(self, evt)



AnkiQt.closeEvent = wrap(AnkiQt.closeEvent, onClose, "around")