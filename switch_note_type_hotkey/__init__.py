from aqt import mw, gui_hooks
from aqt.utils import tooltip


def switch_model(name):
    deck = mw.col
    current = deck.models.current()["name"]
    if current == name:
        return
    m = deck.models.byName(name)
    if m:
        deck.conf["curModel"] = m["id"]
        cdeck = deck.decks.current()
        cdeck["mid"] = m["id"]
        deck.decks.save(cdeck)
        gui_hooks.current_note_type_did_change(current)
        mw.reset()
    else:
        tooltip("No note type with name: " + name)

def run_shortcut(value):
    tooltip(value)
    switch_model(value)

def add_in_shortcuts(cuts, editor):
    config = mw.addonManager.getConfig(__name__)
    for key in config:
        val = config[key]
        cuts.append((key, lambda i=val: run_shortcut(i)))

gui_hooks.editor_did_init_shortcuts.append(add_in_shortcuts)