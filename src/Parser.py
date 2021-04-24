#######################################
#  kiran  >  Parser.py
#  Created by Uygur Kiran on 2021/4/11.
#######################################

from src.Token import *
from src.Error import *
from src.Node import *

#######################################
# PARSE RESULT
#######################################
class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0
        self.last_registered_advance_count = 0
        self.to_reverse_count = 0

    def register_advancement(self):
        self.last_registered_advance_count = 1
        self.advance_count += 1

    def register(self, res):
        self.last_registered_advance_count = res.advance_count
        self.advance_count += res.advance_count
        if res.error: self.error = res.error
        return res.node

    def try_register(self, res):
        if res.error:
            self.to_reverse_count = res.advance_count
            return None
        return self.register(res)

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        if not self.error or self.last_registered_advance_count == 0:
            self.error = error
        return self


#######################################
# PARSER
#######################################
class Parser:
    current_tok: Token

    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self, ):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok

    def update_current_tok(self):
        if 0 <= self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

    def parse(self):
        res = self.__statements()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '+', '-', '*', '/', '§' or '^'"
            ))
        return res

    #######################################
    # PRIVATE METHODS
    #######################################
    # MULTILINE SUPPORT
    def __statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

        # 1ST EXPR
        statement = res.register(self.__statement())
        if res.error: return res
        statements.append(statement)

        # MORE EXPRS
        more_statements = True
        while True:
            newline_count = 0
            while self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()
                newline_count += 1
            if newline_count == 0:
                more_statements = False

            # CHECK END
            if not more_statements: break
            statement = res.try_register(self.__statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(ListNode(
            statements,
            pos_start,
            self.current_tok.pos_end.copy()
        ))


    def __statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.matches(TT_KEYWORD, "RETURN"):
            res.register_advancement()
            self.advance()

            expr = res.try_register(self.__expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))

        if self.current_tok.matches(TT_KEYWORD, "CONTINUE"):
            res.register_advancement()
            self.advance()
            return res.success(ContinueNode(pos_start, self.current_tok.pos_start.copy()))

        if self.current_tok.matches(TT_KEYWORD, "BREAK"):
            res.register_advancement()
            self.advance()
            return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))

        expr = res.register(self.__expr())
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'RETURN', 'CONTINUE', 'BREAK', 'VAR', 'IF', 'FOR', "
                "'WHILE', 'FUNC', int, float, identifier, '+', '-', '(', '[' or 'NOT'"
            ))

        return res.success(expr)


    ## VAR, =, AND, OR
    def __expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'VAR'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier"
                ))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '='"
                ))

            res.register_advancement()
            self.advance()
            expr = res.register(self.__expr())
            if res.error: return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.__bin_op(self.__comp_expr, ((TT_KEYWORD, "AND"), (TT_KEYWORD, "OR"))))

        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'VAR', 'IF', 'FOR', 'WHILE', 'FUNC', int,"
                " float, identifier, '+', '-', '(', '[' or 'NOT'"
            ))

        return res.success(node)


    ## INT, FLOAT & CHECKS FOR KEYWORD EXPRS
    def __atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))

        elif tok.type == TT_STRING:
            res.register_advancement()
            self.advance()
            return res.success(StringNode(tok))

        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.__expr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))

        elif tok.type == TT_LSQUARE:
            list_expr = res.register(self.__list_expr())
            if res.error: return res
            return res.success(list_expr)

        # KEYWORD EXPR CHECKS
        elif tok.matches(TT_KEYWORD, "IF"):
            if_expr = res.register(self.__if_expr())
            if res.error: return res
            return res.success(if_expr)

        elif tok.matches(TT_KEYWORD, "FOR"):
            for_expr = res.register(self.__for_expr())
            if res.error: return res
            return res.success(for_expr)

        elif tok.matches(TT_KEYWORD, "WHILE"):
            while_expr = res.register(self.__while_expr())
            if res.error: return res
            return res.success(while_expr)

        elif tok.matches(TT_KEYWORD, "FUNC"):
            func_expr = res.register(self.__func_def())
            if res.error: return res
            return res.success(func_expr)

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int, float, identifier, '+', '-', '(', '[' "
            "'IF', 'FOR', 'WHILE' or 'FUNC'"
        ))


    ## LIST
    def __list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LSQUARE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '['"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_RSQUARE:
            # [] EMPTY LIST
            res.register_advancement()
            self.advance()
        else:
            # [...]
            element_nodes.append(res.register(self.__expr()))
            if res.error:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']', 'VAR', 'IF', 'FOR', 'WHILE', 'FUNC', "
                    "int, float, identifier, '+', '-', '(', '[' or 'NOT'"
                ))

            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                element_nodes.append(res.register(self.__expr()))
                if res.error: return res

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ']'"
                ))

            res.register_advancement()
            self.advance()

        return res.success(ListNode(
            element_nodes,
            pos_start,
            self.current_tok.pos_end.copy()
        ))


    ## IF...ELSE
    def __if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.__if_expr_cases('IF'))
        if res.error: return res
        cases, else_case = all_cases
        ## PASS NODE WITH ALL CASES
        return res.success(IfNode(cases, else_case))


    def __if_expr_b(self):
        return self.__if_expr_cases('ELIF')


    def __if_expr_c(self):
        res = ParseResult()
        else_case = None

        if self.current_tok.matches(TT_KEYWORD, 'ELSE'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type == TT_NEWLINE:
                res.register_advancement()
                self.advance()

                statements = res.register(self.__statements())
                if res.error: return res
                else_case = (statements, True)

                if self.current_tok.matches(TT_KEYWORD, 'END'):
                    res.register_advancement()
                    self.advance()
                else:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected 'END'"
                    ))
            else:
                expr = res.register(self.__statement())
                if res.error: return res
                else_case = (expr, False)

        return res.success(else_case)


    def __if_expr_b_or_c(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.current_tok.matches(TT_KEYWORD, 'ELIF'):
            all_cases = res.register(self.__if_expr_b())
            if res.error: return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.__if_expr_c())
            if res.error: return res

        return res.success((cases, else_case))


    def __if_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        else_case = None

        # CATCH IF OR ELIF
        if not self.current_tok.matches(TT_KEYWORD, case_keyword):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '{case_keyword}'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.__expr())
        if res.error: return res

        # CATCH THEN
        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        # CATCH SINGLE OR MULTIPLE LINE
        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            statements = res.register(self.__statements())
            if res.error: return res
            # SHOULD RETURN
            cases.append((condition, statements, True))

            # CATCH END OR MORE IF EXPRS
            if self.current_tok.matches(TT_KEYWORD, 'END'):
                res.register_advancement()
                self.advance()
            else:
                all_cases = res.register(self.__if_expr_b_or_c())
                if res.error: return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.__statement())
            if res.error: return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.__if_expr_b_or_c())
            if res.error: return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)

        return res.success((cases, else_case))


    ## FOR LOOP
    def __for_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, "FOR"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'FOR'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected identifier"
            ))

        # NEW VAR-NAME FOUND
        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '='"
            ))

        res.register_advancement()
        self.advance()

        start_value = res.register(self.__expr())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, "TO"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'TO'"
            ))

        res.register_advancement()
        self.advance()

        end_value = res.register(self.__expr())
        if res.error: return res

        # STEP VALUE (OPTIONAL)
        if self.current_tok.matches(TT_KEYWORD, "STEP"):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.__expr())
            if res.error: return res
        else:
            step_value = None

        if not self.current_tok.matches(TT_KEYWORD, "THEN"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        # GET BODY
        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.__statements())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'END'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'END'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))

        body = res.register(self.__statement())
        if res.error: return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body, False))


    ## WHILE LOOP
    def __while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, "WHILE"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'WHILE'"
            ))

        res.register_advancement()
        self.advance()

        condition = res.register(self.__expr())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'THEN'"
            ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_advancement()
            self.advance()

            body = res.register(self.__statements())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'END'):
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'END'"
                ))

            res.register_advancement()
            self.advance()

            return res.success(WhileNode(condition, body, True))

        body = res.register(self.__statement())
        if res.error: return res

        return res.success(WhileNode(condition, body, False))


    # FUNC CALL
    def __call(self):
        res = ParseResult()
        atom = res.register(self.__atom())
        if res.error: return res

        if self.current_tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            arg_nodes = []
            # IF () NO ARGS
            if self.current_tok.type == TT_RPAREN:
                res.register_advancement()
                self.advance()
            else:
                # (...) ARG
                arg_nodes.append(res.register(self.__expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ')', 'VAR', 'IF', 'FOR', 'WHILE', 'FUNC', "
                        "int, float, identifier, '+', '-', '(', '[' or 'NOT'"
                    ))
                # MORE ARGS
                while self.current_tok.type == TT_COMMA:
                    res.register_advancement()
                    self.advance()

                    arg_nodes.append(res.register(self.__expr()))
                    if res.error: return res

                if self.current_tok.type != TT_RPAREN:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected ',' or ')'"
                    ))

                res.register_advancement()
                self.advance()

            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)


    ## EXPONENTIATION
    def __power(self):
        return self.__bin_op(self.__call, (TT_POW,), self.__factor)


    ## UNARY OPERATION
    def __factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.__factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        return self.__power()

    def __term(self):
        return self.__bin_op(self.__factor, (TT_MUL, TT_DIV, TT_SAFEDIV))

    def __arith_expr(self):
        return self.__bin_op(self.__term, (TT_PLUS, TT_MINUS))


    ## COMPARISON
    def __comp_expr(self):
        res = ParseResult()
        # IF "NOT"
        if self.current_tok.matches(TT_KEYWORD, "NOT"):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.__comp_expr())
            if res.error: return res
            # -> NOT, NODE
            return res.success(UnaryOpNode(op_tok, node))

        node = res.register(self.__bin_op(self.__arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
        if res.error:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected int, float, identifier, '+', '-','(', '[' or 'NOT'"))
        return res.success(node)


    ## FUNC
    def __func_def(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, "FUNC"):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'FUNC'"
            ))
        # "FUNC" FOUND
        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_IDENTIFIER:
            # HAVE FUNC-NAME
            var_name_tok = self.current_tok
            res.register_advancement()
            self.advance()
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected '('"
                ))
        else:
            # NO NAME
            var_name_tok = None
            if self.current_tok.type != TT_LPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier or '('"
                ))

        res.register_advancement()
        self.advance()
        arg_name_toks = []

        # ARGS
        if self.current_tok.type == TT_IDENTIFIER:
            arg_name_toks.append(self.current_tok)
            res.register_advancement()
            self.advance()
            # MORE ARGS
            while self.current_tok.type == TT_COMMA:
                res.register_advancement()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        f"Expected identifier"
                    ))

                arg_name_toks.append(self.current_tok)
                res.register_advancement()
                self.advance()

            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected ',' or ')'"
                ))
        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected identifier or ')'"
                ))

        res.register_advancement()
        self.advance()

        if self.current_tok.type == TT_ARROW:
            res.register_advancement()
            self.advance()

            body = res.register(self.__expr())
            if res.error: return res

            return res.success(FuncDefNode(
                var_name_tok,
                arg_name_toks,
                body,
                True
            ))

        if self.current_tok.type != TT_NEWLINE:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '->' or NEWLINE"
            ))

        res.register_advancement()
        self.advance()

        body = res.register(self.__statements())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'END'):
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'END'"
            ))

        res.register_advancement()
        self.advance()

        return res.success(FuncDefNode(
            var_name_tok,
            arg_name_toks,
            body,
            False
        ))



    ## BINARY OPERATION
    def __bin_op(self, func_a, ops, func_b=None):
        if func_b is None:
            func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)
