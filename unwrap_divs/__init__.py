from aqt import gui_hooks


def inject_code(self):
    c = len(self.note.fields)
    self.web.eval("""
(function(){
    removeDiv = function(str){
        while(true){
            reg = /<div>([\s\S]*?)<\/div>/g;
                        oldStr = str
            str = str.replace(reg,'$1');
                        if(str == oldStr){
                            break;
            }
        }
        return str
    }

    for(var x = 0; x < %d; x++){
        el = document.getElementById("f"+x);
        el.addEventListener('keyup',function(event){
            key = event.code
            if(key == "Backspace" || key == "Delete"){
                html = el.innerHTML
                newHtml = removeDiv(html)
                if(html != newHtml){
                    el.innerHTML = html
                }
            }
        }

    }
})()
    
"""%c)

gui_hooks.editor_did_load_note.append(inject_code)