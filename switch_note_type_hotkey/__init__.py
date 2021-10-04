from typing import Optional
from aqt import mw, gui_hooks
from aqt.utils import tooltip
from aqt.addcards import AddCards

add_dialog: Optional[AddCards] = None

def switch_model(name):
    notetype = mw.col.models.by_name(name)
    if notetype:
        id = notetype["id"]
        add_dialog.notetype_chooser.selected_notetype_id = id
    else:
        tooltip("No note type with name: " + name)
        
def run_shortcut(value):
    tooltip(value)
    switch_model(value)

def add_in_shortcuts(cuts, editor):
    myscuts = mw.addonManager.getConfig(__name__)["shortcuts"]
    for key in myscuts:
        val = myscuts[key]
        if val and val != "none":
            cuts.append((key, lambda i=val: run_shortcut(i)))

def new_add_cards(addcards: AddCards):
    global add_dialog
    add_dialog = addcards


gui_hooks.add_cards_did_init.append(new_add_cards)
gui_hooks.editor_did_init_shortcuts.append(add_in_shortcuts)