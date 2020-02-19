from aqt.deckbrowser import DeckBrowser
from anki.hooks import wrap

from aqt.utils import tooltip


class magical_question_mark:

    def __add__(self, other):
        return self

    def __ge__(self, other):
        if other == 1000:
            return False
        else:
            raise Exception("Anki Code changed!")
    
    def __str__(self):
        return "?"

def myfunc(self, node, *args, _old, **kwargs):
    #node is a tuple
    #name, did, due, lrn, new, children
    a = list(node)
    tooltip("a")
    if a[2] + a[3]:
        a[2] = magical_question_mark()
        a[4] = magical_question_mark()
        node = tuple(a)
    return _old(self, node, *args, **kwargs)

DeckBrowser._deckRow = wrap(DeckBrowser._deckRow, myfunc, "around")