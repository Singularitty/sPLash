from lark import Transformer
from typing import List, Tuple
from parser.ast_nodes import *




class AstTransformer(Transformer):

    ### Expressions - Literals/Values

    def ID(self, item) -> IdentifierExprNode:
        return IdentifierExprNode(item.line, item.column, item.value)

    def FLOATLIT(self, item) -> FloatLiteralExprNode:
        value = float(item.value)
        return FloatLiteralExprNode(item.line, item.column, value)

    def INTLIT(self, item) -> IntLiteralExprNode:
        value = int(item.value)
        return IntLiteralExprNode(item.line, item.column, value)

    def STRING(self, item) -> StrExprNode:
        return StrExprNode(item.line, item.column, item.value)

    def true(self, item) -> BoolLiteralExprNode:
        assert (item.value == "true")
        return BoolLiteralExprNode(item.line, item.column, True)

    def false(self, item) -> BoolLiteralExprNode:
        assert (item.value == "false")
        return BoolLiteralExprNode(item.line, item.column, False)

    # Function Arguments

    def func_arguments(self, items) -> List[ExprNode]:
        return items

    def parameters(self, items) -> List[Tuple[IdentifierExprNode, TypeNode]]:
        if len(items) == 0:
            return items
        assert len(items) % 2 == 0
        args = []
        items_it = iter(items)
        # Turn list into iterator, so we can iterate through two items at a time
        for x in items_it:
            # Make pair of Identifier and Type
            args.append((x, next(items_it)))
        return args

    # Expressions - Function Returns

    def function_return(self, items) -> FuncReturnExprNode:
        identifier = items[0]
        args = items[1]
        return FuncReturnExprNode(identifier.line, identifier.column, identifier, args)

    # Expressions - Index Access

    def index_access(self, items) -> IndexAccessExprNode:
        identifier = items[0]
        index = items[1]
        return IndexAccessExprNode(identifier.line, identifier.column, identifier, index)

    def index_access_func(self, items) -> IndexAccessExprNode:
        func_return = items[0]
        index = items[1]
        return IndexAccessExprNode(func_return.line, func_return.column, func_return, index)

    # Expressions - Unary Operations

    def unary_not(self, items) -> UnaryExprNode:
        operator = UnaryOperator.NOT
        exp = items[0]
        return UnaryExprNode(exp.line, exp.column, exp, operator)

    # Expressions - Binary Operations

    def bin_plus(self, items) -> BinaryExprNode:
        expr1 = items[0]
        expr2 = items[1]
        operator = BinaryOperator.PLUS
        return BinaryExprNode(expr1.line, expr1.column, expr1, operator, expr2)

    def bin_minus(self, items) -> BinaryExprNode:
        expr1 = items[0]
        expr2 = items[1]
        operator = BinaryOperator.MINUS
        return BinaryExprNode(expr1.line, expr1.column, expr1, operator, expr2)

    def bin_multiplication(self, items) -> BinaryExprNode:
        expr1 = items[0]
        expr2 = items[1]
        operator = BinaryOperator.MUL
        return BinaryExprNode(expr1.line, expr1.column, expr1, operator, expr2)

    def bin_divison(self, items) -> BinaryExprNode:
        expr1 = items[0]
        expr2 = items[1]
        operator = BinaryOperator.DIV
        return BinaryExprNode(expr1.line, expr1.column, expr1, operator, expr2)

    def bin_modulus(self, items) -> BinaryExprNode:
        expr1 = items[0]
        expr2 = items[1]
        operator = BinaryOperator.MOD
        return BinaryExprNode(expr1.line, expr1.column, expr1, operator, expr2)

    def bin_equals(self, items) -> BinaryExprNode:
        expr1 = items[0]
        expr2 = items[1]
        operator = BinaryOperator.EQ
        return BinaryExprNode(expr1.line, expr1.column, expr1, operator, expr2)

    def bin_not_equals(self, items) -> BinaryExprNode:
        expr1 = items[0]
        expr2 = items[1]
        operator = BinaryOperator.NEQ
        return BinaryExprNode(expr1.line, expr1.column, expr1, operator, expr2)

    def bin_greather_equals(self, items) -> BinaryExprNode:
        expr1 = items[0]
        expr2 = items[1]
        operator = BinaryOperator.GE
        return BinaryExprNode(expr1.line, expr1.column, expr1, operator, expr2)

    def bin_greather(self, items) -> BinaryExprNode:
        expr1 = items[0]
        expr2 = items[1]
        operator = BinaryOperator.GT
        return BinaryExprNode(expr1.line, expr1.column, expr1, operator, expr2)

    def bin_less_equals(self, items) -> BinaryExprNode:
        expr1 = items[0]
        expr2 = items[1]
        operator = BinaryOperator.LE
        return BinaryExprNode(expr1.line, expr1.column, expr1, operator, expr2)

    def bin_less(self, items) -> BinaryExprNode:
        expr1 = items[0]
        expr2 = items[1]
        operator = BinaryOperator.LT
        return BinaryExprNode(expr1.line, expr1.column, expr1, operator, expr2)

    def bin_and(self, items) -> BinaryExprNode:
        expr1 = items[0]
        expr2 = items[1]
        operator = BinaryOperator.AND
        return BinaryExprNode(expr1.line, expr1.column, expr1, operator, expr2)

    def bin_or(self, items) -> BinaryExprNode:
        expr1 = items[0]
        expr2 = items[1]
        operator = BinaryOperator.OR
        return BinaryExprNode(expr1.line, expr1.column, expr1, operator, expr2)

    # Types

    def type(self, items) -> TypeNode:
        refinement = None
        if len(items) == 2:
            refinement = items[1]
        return TypeNode(items[0].line, items[0].column, items[0], refinement)

    def type_name(self, items) -> TypeNameNode:
        return TypeNameNode(items[0].line, items[0].column, items[0])

    def array(self, items) -> ArrayTypeNode:
        return ArrayTypeNode(items[0].line, items[0].column, items[0])


    # Block

    def block(self, items) -> BlockNode:
        if len(items) > 0:
            return BlockNode(items[0].line, items[0].column, items)
        else:
            return BlockNode(items[1].line, items[1].column, [])

    ### Statements - Assignments

    def assignment(self, items) -> VariableAssignmentStmtNode:
        var_id = items[0]
        expr = items[1]
        return VariableAssignmentStmtNode(var_id.line, var_id.column, var_id, expr)

    ### Statements - If

    def if_statement(self, items) -> IfStmtNode:
        conditional = items[0]
        then_block = items[1]
        if len(items) == 3:
            else_block = items[2]
        else:
            else_block = None
        return IfStmtNode(conditional.line, conditional.column, conditional, then_block, else_block)

    ### Statements - While

    def while_statement(self, items) -> WhileStmtNode:
        guard = items[0]
        do_block = items[1]
        return WhileStmtNode(guard.line, guard.column, guard, do_block)

    ### Statements - Expressions

    def exp_statement(self, item) -> ExprStmtNode:
        return ExprStmtNode(item[0].line, item[0].column, item[0])

    ### Statements - Return

    def return_statement(self, item) -> ReturnStmtNode:
        return ReturnStmtNode(item[0].line, item[0].column, item[0])

    # Statements - Local Value Definiton

    def local_def_statement(self, items) -> LocalValueDefinitionNode:
        identifier = items[0]
        type_id = items[1]
        expr = items[2]
        return LocalValueDefinitionNode(identifier.line, identifier.column, identifier, type_id, expr)

    ### Definitions - Value

    def value_def(self, items) -> ValueDefinitionNode:
        identifier = items[0]
        type_id = items[1]
        expr = items[2]
        return ValueDefinitionNode(identifier.line, identifier.column, identifier, type_id, expr)

    ### Definitions - Functions

    def function_def(self, items) -> FunctionDefinitionNode:
        func_id = items[0]
        type_id = items[1]
        args = items[2]
        body = items[3]
        return FunctionDefinitionNode(func_id.line, func_id.column, func_id, type_id, args, body)
        

    ### Declarations - Variable

    def var_declaration(self, items) -> VariableDeclarationNode:
        var_id = items[0]
        type_id = items[1]
        return VariableDeclarationNode(var_id.line, var_id.column, var_id, type_id)

    ### Declarations - Function

    def function_declaration(self, items) -> FunctionDeclarationNode:
        func_id = items[0]
        type_id = items[1]
        args = items[2]
        return FunctionDeclarationNode(func_id.line, func_id.column, func_id, type_id, args)

    # Main

    # It's the same as a function definition, but ProgramNode will later assert its id is "main"
    def main_body(self, items) -> FunctionDefinitionNode:
        main_id = items[0]
        type_id = items[1]
        args = items[2]
        body = items[3]
        return FunctionDefinitionNode(main_id.line, main_id.column, main_id, type_id, args, body)

    # Program

    def start(self, items) -> ProgramNode:
        program_body = items[:-1]
        main = items[-1]
        return ProgramNode(items[0].line, items[0].column, program_body, main)
