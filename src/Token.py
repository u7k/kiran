#######################################
#  kiran  >  Token.py
#  Created by Uygur Kiran on 2021/4/11.
#######################################

#######################################
# TOKEN TYPES
#######################################
TT_INT = "INT"
TT_FLOAT = "FLOAT"
TT_STRING = "STRING"
TT_IDENTIFIER = "IDENTIFIER"
TT_KEYWORD = "KEYWORD"

# ARITHMETIC
TT_PLUS = "PLUS"
TT_MINUS = "MINUS"
TT_MUL = "MUL"
TT_DIV = "DIV"
TT_SAFEDIV = "SAFEDIV"
TT_POW = "POW"

# COMPARISON
TT_EE = "EE"    # ==
TT_NE = "NE"    # !=
TT_LT = "LT"    # <
TT_GT = "GT"    # >
TT_LTE = "LTE"  # <=
TT_GTE = "GTE"  # >=

# MULTI PURPOSE
TT_EQ = "EQ"    # =
TT_LPAREN = "LPAREN"
TT_RPAREN = "RPAREN"

# LIST
TT_LSQUARE = 'LSQUARE'
TT_RSQUARE = 'RSQUARE'

# FUNC
TT_COMMA = "COMMA"
TT_ARROW = "ARROW"
TT_NEWLINE = "NEWLINE"

# END OF LINE
TT_EOF = "EOF"

#######################################
# KEYWORDS
#######################################
KEYWORDS = [
    "VAR",
    "AND",
    "OR",
    "NOT",
    "IF",
    "THEN",
    "ELIF",
    "ELSE",
    "FOR",
    "TO",
    "STEP",
    "WHILE",
    "FUNC",
    "END",
    "RETURN",
    "CONTINUE",
    "BREAK"
]

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