#######################################
#  kiran  >  Interpreter.py
#  Created by Uygur Kiran on 2021/4/11
#######################################

from src.Token import *
from src.Number import *

#######################################
# INTERPRETER
#######################################
class Interpreter:
    def visit(self, node, context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f"No visit_{type(node).__name__} method defined.")

    def visit_NumberNode(self, node, context):
        return RuntimeResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    ## GET VALUE (VAR)
    def visit_VarAccessNode(self, node, context):
        res = RuntimeResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RunTimeError(
                node.pos_start, node.pos_end,
                f"{var_name} is not defined",
                context
            ))

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    ## ASSIGN VALUE (VAR)
    def visit_VarAssignNode(self, node, context):
        res = RuntimeResult()
        var_name = node.var_name_tok.value
        value = res.register( self.visit(node.value_node, context) )
        if res.error: return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_BinOpNode(self, node, context):
        res = RuntimeResult()

        # ACCESS CHILD NODES -> Number
        left = res.register(self.visit(node.left_node, context))
        if res.error: return res
        right = res.register(self.visit(node.right_node, context))
        if res.error: return res

        # DETERMINE OPERATION
        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        elif node.op_tok.type == TT_SAFEDIV:
            result, error = left.safe_dived_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.powed_by(right)
            ## LOGICAL & COMP. OPERATIONS
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TT_KEYWORD, "AND"):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, "OR"):
            result, error = left.ored_by(right)

        if error:
            return res.failure(error)
        else:
            # -> RuntimeResult -> NUM
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RuntimeResult()

        # ACCESS CHILD NODE
        number = res.register(self.visit(node.node, context))
        if res.error: return res

        error = None
        if node.op_tok.type == TT_MINUS:
            # NEGATE NUM IF -
            number, error = number.multed_by(Number(-1))
        elif node.op_tok.matches(TT_KEYWORD, 'NOT'):
            number, error = number.notted()

        if error:
            return res.failure(error)
        else:
            # -> RuntimeResult -> NUM
            return res.success( number.set_pos(node.pos_start, node.pos_end) )

    ## IF...ELSE
    def visit_IfNode(self, node, context):
        res = RuntimeResult()

        for condition, expr in node.cases:
            # GET CONDITION VALUE
            condition_value = res.register(self.visit(condition, context))
            if res.error: return res

            # CHECK CONDITION
            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(expr_value)

        # OR PROCEED TO ELSE-CASE
        if node.else_case:
            else_value = res.register(self.visit(node.else_case, context))
            if res.error: return res
            return res.success(else_value)

        # IF NO ELSE-CASE
        return res.success(None)