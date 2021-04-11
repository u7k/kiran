#######################################
#  kiran  >  Context.py
#  Created by Uygur Kiran on 2021/4/11
#######################################

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos