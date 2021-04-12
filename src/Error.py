#######################################
#  kiran  >  Error.py
#  Created by Uygur Kiran on 2021/4/11.
#######################################

from style.string_with_arrows import string_with_arrows

#######################################
# MODEL
#######################################
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f"{self.error_name}: {self.details}\n"
        result += f"File {self.pos_start.fn}, line {self.pos_start.ln + 1}"
        result += "\n\n" + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

#######################################
# ERROR TYPES
#######################################
class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Illegal Character", details)

class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "Expected Character", details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=""):
        super().__init__(pos_start, pos_end, "Invalid Syntax", details)

class RunTimeError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', details)
        self.context = context

    # OVERRIDE AS_STR()
    def as_string(self):
        result = self.generate_traceback()
        result += f"{self.error_name}: {self.details}\n"
        result += "\n\n" + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

    def generate_traceback(self):
        result = ""
        pos = self.pos_start
        context = self.context
        # LOOP UNTIL NO PARENT LEFT
        while context:
            result = f"    File {pos.fn}, line {pos.ln + 1}, in {context.display_name}\n" + result
            pos = context.parent_entry_pos
            context = context.parent

        return "Traceback (most recent call last):\n" + result


#######################################
# RUNTIME RESULT
#######################################
class RuntimeResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, res):
        if res.error: self.error = res.error
        return res.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self
