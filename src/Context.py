#######################################
#  kiran  >  Context.py
#  Created by Uygur Kiran on 2021/4/11
#######################################

#######################################
# CONTEXT
#######################################
class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        # TRACK VARS
        self.symbol_table = None


#######################################
# SYMBOL TABLE
#######################################
class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.parent = None

    # GET VAR VALUE
    def get(self, name):
        value = self.symbols.get(name, None)
        if value == None and self.parent:
            return self.parent.get(name)
        return value

    # STORE VAR VALUE
    def set(self, name, value):
        self.symbols[name] = value

    def remove(self, name):
        del self.symbols[name]


