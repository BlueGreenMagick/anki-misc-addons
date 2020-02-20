from aqt.deckbrowser import DeckBrowser
from aqt.overview import Overview
from anki.hooks import wrap

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

def browserfunc(self, node, *args, _old, **kwargs):
    #node is a tuple
    #name, did, due, lrn, new, children
    a = list(node)
    if a[2] + a[3]:
        a[2] = magical_question_mark()
    if a[4]:    
        a[4] = magical_question_mark()
    node = tuple(a)
    return _old(self, node, *args, **kwargs)

def overviewfunc(self, _old):
    r = _old(self)
    return r + """
<script>
    (function(){
        var hideCount = function(str){
            el = document.getElementsByClassName(str)[0];
            if(el.innerHTML != "0"){
                el.innerHTML = "?";
            }
        }
        var classes = ["new-count", "learn-count", "review-count"];
        for(var x = 0; x < classes.length; x++){
            hideCount(classes[x]);
        }
    })()
</script>
"""

DeckBrowser._deckRow = wrap(DeckBrowser._deckRow, browserfunc, "around")
Overview._table = wrap(Overview._table, overviewfunc, "around")