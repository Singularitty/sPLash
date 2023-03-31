from abc import ABC
from typing import List, Tuple
from enum import Enum

# Opeprators

class BinaryOperator(Enum):
    PLUS   = 1
    MINUS  = 2
    MUL    = 3
    DIV    = 4
    MOD    = 5
    EQ     = 6
    NEQ    = 7
    GE     = 8
    GT     = 9
    LE     = 10
    LQ     = 11
    AND    = 12
    OR     = 13

class UnaryOperator(Enum):
    NOT = 1


# Abstract Syntax Tree Nodes

class Node(ABC):
    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

# Expressions

class ExprNode(Node):
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)

class IntLiteralExprNode(ExprNode):
    def __init__(self, line: int, column: int, value: int) -> None:
        super().__init__(line, column)
        self.value = value

class SignedIntLiteralExprNode(IntLiteralExprNode):
    def __init__(self, line: int, column: int, value: int, sign: str) -> None:
        super().__init__(line, column, value)
        assert sign in ("+","-")
        self.sign = sign

class FloatLiteralExprNode(ExprNode):
    def __init__(self, line: int, column: int, value: float) -> None:
        super().__init__(line, column)
        self.value = value

class SignedFloatLiteralExprNode(FloatLiteralExprNode):
    def __init__(self, line: int, column: int, value: float, sign: str) -> None:
        super().__init__(line, column, value)
        assert sign in ("+","-")
        self.sign = sign

class BoolLiteralExprNode(ExprNode):
    def __init__(self, line: int, column: int, value: bool) -> None:
        super().__init__(line, column)
        self.value = value

class StrExprNode(ExprNode):
    def __init__(self, line: int, column: int, value: str) -> None:
        super().__init__(line, column)
        self.value = value

class IdentifierExprNode(ExprNode):
    def __init__(self, line: int, column: int, identifier: str) -> None:
        super().__init__(line, column)
        self.identifier = identifier

class FuncReturnExprNode(ExprNode):
    def __init__(self, line: int, column: int, func_id: str, args: List[ExprNode]) -> None:
        super().__init__(line, column)
        assert all(isinstance(n, ExprNode) for n in args)
        self.func_name = func_id
        self.args = args

class BinaryExprNode(ExprNode):
    def __init__(self, line: int, column: int, expr1: ExprNode, operator: BinaryOperator, expr2: ExprNode) -> None:
        super().__init__(line, column)
        assert isinstance(expr1, ExprNode)
        assert isinstance(expr2, ExprNode)
        assert isinstance(operator, BinaryOperator)
        self.expr1 = expr1
        self.expr2 = expr2
        self.operator = operator
    
class UnaryExprNode(ExprNode):
    def __init__(self, line: int, column: int, expr: ExprNode, operator: UnaryOperator) -> None:
        super().__init__(line, column)
        assert isinstance(expr, ExprNode)
        assert isinstance(operator, UnaryOperator)
        self.expr = expr
        self.operator = operator

class IndexAccessExprNode(ExprNode):
    def __init__(self, line: int, column: int, array: ExprNode, index: ExprNode) -> None:
        super().__init__(line, column)
        assert isinstance(array, ExprNode)
        assert isinstance(index, ExprNode)
        self.array = array
        self.index = index

# Types

class TypeNode(Node):
    def __init__(self, line: int, column: int, type_name: str) -> None:
        super().__init__(line, column)
        self.type_name = type_name

class RefinedTypeNode(TypeNode):
    def __init__(self, line: int, column: int, type_name: str, refinement: ExprNode) -> None:
        super().__init__(line, column, type)
        assert isinstance(refinement, ExprNode)
        self.type_name = type_name
        self.refinement = refinement

# Declarations

class DeclarationNode(Node):
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)


class FunctionDeclarationNode(DeclarationNode):
    def __init__(self, line: int, column: int, func_id: str, type_: TypeNode, req_args: List[Tuple(str, TypeNode)]) -> None:
        super().__init__(line, column)
        assert isinstance(type_, TypeNode)
        assert all(isinstance(arg[1], TypeNode) for arg in req_args)
        self.func_id = func_id
        self.type_ = type_
        self.req_args = req_args

class VariableDeclarationNode(DeclarationNode):
    def __init__(self, line: int, column: int, var_id: str, type_: TypeNode) -> None:
        super().__init__(line, column)
        assert isinstance(type_, TypeNode)
        self.var_id = var_id
        self.type_ = type_


# Statements


class StmtNode(Node):
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)

class BlockNode(Node):
    def __init__(self, line: int, column: int, statements: List[StmtNode]) -> None:
        super().__init__(line, column)
        assert all(isinstance(n, StmtNode) for n in statements)
        self.statements = statements

class LocalVariableDeclarationNode(StmtNode):
    def __init__(self, line: int, column: int, var_id: str, type_: TypeNode) -> None:
        super().__init__(line, column)
        assert isinstance(type_, TypeNode)
        self.var_id = var_id
        self.type_ = type_

class VariableAssignmentStmtNode(StmtNode):
    def __init__(self, line: int, column: int, var_id: str, expr: ExprNode) -> None:
        super().__init__(line, column)
        assert isinstance(expr, ExprNode)
        self.var_id = var_id
        self.expr = expr

class ExprStmtNode(StmtNode):
    def __init__(self, line: int, column: int, expr: ExprNode) -> None:
        super().__init__(line, column)
        assert isinstance(expr, ExprNode)
        self.expr = expr

class ReturnStmtNode(StmtNode):
    def __init__(self, line: int, column: int, return_expr: ExprNode) -> None:
        super().__init__(line, column)
        assert isinstance(return_expr, ExprNode)
        self.return_expr = return_expr

class IfStmtNode(StmtNode):
    def __init__(self, line: int, column: int, conditional: ExprNode, then_block: BlockNode, else_block: BlockNode | None) -> None:
        super().__init__(line, column)
        assert isinstance(conditional, ExprNode)
        assert isinstance(then_block, BlockNode)
        self.conditional = conditional
        self.then_block = then_block
        if else_block is not None:
            assert isinstance(else_block, BlockNode)
            self.else_block = else_block
        else:
            self.else_block = None

class WhileStmtNode(StmtNode):
    def __init__(self, line: int, column: int, guard: ExprNode, do_block: BlockNode) -> None:
        super().__init__(line, column)
        assert isinstance(guard, ExprNode)
        assert isinstance(do_block, ExprNode)
        self.guard = guard
        self.do_block = do_block


# Definitions

class DefinitionNode(Node):
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)

class FunctionDefinitionNode(DefinitionNode):
    def __init__(self, line: int, column: int, func_id: str, type_: TypeNode, body: BlockNode) -> None:
        super().__init__(line, column)
        assert isinstance(type_, TypeNode)
        assert isinstance(body, BlockNode)
        self.func_id = func_id
        self.type_ = type_
        self.body = body

class ValueDefinitionNode(DefinitionNode):
    def __init__(self, line: int, column: int, var_id: str, type_: TypeNode, expr: ExprNode) -> None:
        super().__init__(line, column)
        assert isinstance(type_, TypeNode)
        assert isinstance(expr, ExprNode)
        self.var_id = var_id
        self.type_ = type_
        self.expr = expr

# Program

class ProgramNode(Node):
    def __init__(self, line: int, column: int, program_body: List[DeclarationNode | DefinitionNode], main: FunctionDefinitionNode) -> None:
        super().__init__(line, column)
        assert all((isinstance(n, DeclarationNode) or isinstance(n, DefinitionNode) for n in program_body))
        self.program_body = program_body
        assert isinstance(main, FunctionDefinitionNode)
        assert main.func_id == "main"
        self.main = main
