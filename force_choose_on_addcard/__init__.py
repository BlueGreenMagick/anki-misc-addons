from anki.hooks import wrap
from aqt import mw
from aqt.addcards import AddCards

config = mw.addonManager.getConfig(__name__)

def newinit(self, mw, _old):
    _old(self, mw)

    #The order is important
    if config["deck"]:
        self.deckChooser.onDeckChange()
    if config["model"]:
        self.modelChooser.onModelChange()
    
AddCards.__init__ = wrap(AddCards.__init__, newinit, "around")