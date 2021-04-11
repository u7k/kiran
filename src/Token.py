#######################################
#  kiran  >  Token.py
#  Created by Uygur Kiran on 2021/4/11.
#######################################

#######################################
# TOKEN TYPES
#######################################
TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"

TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_SAFEDIV = "SAFEDIV"
TT_POW = "POW"

TT_EQ = "EQ"
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"
TT_EOF = "EOF"

#######################################
# KEYWORDS
#######################################
KEYWORDS = [ "VAR" ]

#######################################
# MODEL
#######################################
class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        if pos_start:
            self.pos_start = pos_start.copy()
            ## default end pos.
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        if pos_end:
            ## assigned end pos.
            self.pos_end = pos_end

    ## CHECK FOR KEYWORDS
    def matches(self, type_, value):
        return bool(self.type == type_ and self.value == value)

    def __repr__(self):
        if self.value: return f"{self.type}:{self.value}"
        return f"{self.type}"