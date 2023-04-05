from abc import ABC, abstractmethod
from typing import List, Tuple
from enum import Enum
import json


class ComplexEncoder(json.JSONEncoder):
    """
    This class is used by json.dumps() to call an objects reprJSON() method
    when it is determined that object has such a method. By doing this classes
    with reprJSON method can return a JSON representation.

    This allows the representation of nested objects with JSON.
    """

    def default(self, o):
        if hasattr(o, 'reprJSON'):
            return o.reprJSON()
        return json.JSONEncoder.default(self, o)

# Opeprators
# These are Enums but they inherit from str class to have native Json representation

class BinaryOperator(str, Enum):
    PLUS = "+"
    MINUS = "-"
    MUL = "*"
    DIV = "/"
    MOD = "%"
    EQ = "=="
    NEQ = "!="
    GE = ">="
    GT = ">"
    LE = "<="
    LT = "<"
    AND = "&&"
    OR = "||"

class UnaryOperator(str, Enum):
    NOT = "!"

# We will later need to distinguish if a type refers to a single value or an array for type checking
# Instead of creating IntArray, etc... We allow an array to have any type of items. Except void of course.
class DataType(str, Enum):
    value = "value"
    array = "array"


# Abstract Syntax Tree Nodes

class Node(ABC):
    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

    # All subclasses of Node, must have reprJSON implemented in order to return
    # a JSON representation
    @abstractmethod
    def reprJSON(self):
        pass

# Expressions


class ExprNode(Node):
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)

    @abstractmethod
    def reprJSON(self):
        pass


class IntLiteralExprNode(ExprNode):
    def __init__(self, line: int, column: int, value: int) -> None:
        super().__init__(line, column)
        self.value = value

    def reprJSON(self):
        return {"node": self.__class__.__name__, "value": self.value}


class SignedIntLiteralExprNode(IntLiteralExprNode):
    def __init__(self, line: int, column: int, value: int, sign: str) -> None:
        super().__init__(line, column, value)
        assert sign in ("+", "-")
        self.sign = sign

    def reprJSON(self):
        return {"node": self.__class__.__name__, "sign": self.sign, "value": self.value}


class FloatLiteralExprNode(ExprNode):
    def __init__(self, line: int, column: int, value: float) -> None:
        super().__init__(line, column)
        self.value = value

    def reprJSON(self):
        return {"node": self.__class__.__name__, "value": self.value}


class SignedFloatLiteralExprNode(FloatLiteralExprNode):
    def __init__(self, line: int, column: int, value: float, sign: str) -> None:
        super().__init__(line, column, value)
        assert sign in ("+", "-")
        self.sign = sign

    def reprJSON(self):
        return {"node": self.__class__.__name__, "sign": self.sign, "value": self.value}


class BoolLiteralExprNode(ExprNode):
    def __init__(self, line: int, column: int, value: bool) -> None:
        super().__init__(line, column)
        self.value = value

    def reprJSON(self):
        return {"node": self.__class__.__name__, "value": self.value}


class StrExprNode(ExprNode):
    def __init__(self, line: int, column: int, value: str) -> None:
        super().__init__(line, column)
        self.value = value

    def reprJSON(self):
        return {"node": self.__class__.__name__, "value": self.value}


class IdentifierExprNode(ExprNode):
    def __init__(self, line: int, column: int, identifier: str) -> None:
        super().__init__(line, column)
        self.identifier = identifier

    def reprJSON(self):
        return {"node": self.__class__.__name__, "identifier": self.identifier}


class FuncReturnExprNode(ExprNode):
    def __init__(self, line: int, column: int, func_id: str, arguments: List[ExprNode]) -> None:
        super().__init__(line, column)
        assert all(isinstance(n, ExprNode) for n in arguments)
        self.func_name = func_id
        self.arguments = arguments

    def reprJSON(self):
        return {"node": self.__class__.__name__, "function identifier": self.func_name, "arguments": self.arguments}


class BinaryExprNode(ExprNode):
    def __init__(self, line: int, column: int, expr1: ExprNode, operator: BinaryOperator, expr2: ExprNode) -> None:
        super().__init__(line, column)
        assert isinstance(expr1, ExprNode)
        assert isinstance(expr2, ExprNode)
        assert isinstance(operator, BinaryOperator)
        self.expr1 = expr1
        self.expr2 = expr2
        self.operator = operator

    def reprJSON(self):
        return {"node": self.__class__.__name__, "operator": self.operator, "left expression": self.expr1, "right expression": self.expr2}


class UnaryExprNode(ExprNode):
    def __init__(self, line: int, column: int, expr: ExprNode, operator: UnaryOperator) -> None:
        super().__init__(line, column)
        assert isinstance(expr, ExprNode)
        assert isinstance(operator, UnaryOperator)
        self.expr = expr
        self.operator = operator

    def reprJSON(self):
        return {"node": self.__class__.__name__, "operator": self.operator, "expression": self.expr}


class IndexAccessExprNode(ExprNode):
    def __init__(self, line: int, column: int, array: ExprNode, index: ExprNode) -> None:
        super().__init__(line, column)
        assert isinstance(array, ExprNode)
        assert isinstance(index, ExprNode)
        self.array = array
        self.index = index

    def reprJSON(self):
        return {"node": self.__class__.__name__, "identifier": self.array, "index": self.index}

# Types


class TypeNode(Node):
    def __init__(self, line: int, column: int, type_id: IdentifierExprNode, data_type: DataType) -> None:
        super().__init__(line, column)
        self.type_id = type_id
        self.data_type = data_type

    def reprJSON(self):
        return {"node": self.__class__.__name__, "data type" : self.data_type,  "type": self.type_id}


class RefinedTypeNode(TypeNode):
    def __init__(self, line: int, column: int, type_id: IdentifierExprNode, data_type: DataType, refinement: ExprNode) -> None:
        super().__init__(line, column, type_id, data_type)
        assert isinstance(refinement, ExprNode)
        self.refinement = refinement

    def reprJSON(self):
        return {"node": self.__class__.__name__, "data type" : self.data_type, "type": self.type_id, "refinement": self.refinement}

# Declarations


class DeclarationNode(Node):
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)

    @abstractmethod
    def reprJSON(self):
        pass


class FunctionDeclarationNode(DeclarationNode):
    def __init__(self, line: int, column: int, func_id: str, type_: TypeNode, parameters: List[Tuple[IdentifierExprNode, TypeNode]]) -> None:
        super().__init__(line, column)
        assert isinstance(type_, TypeNode)
        assert all(isinstance(arg[0], IdentifierExprNode)
                   for arg in parameters)
        assert all(isinstance(arg[1], TypeNode) for arg in parameters)
        self.func_id = func_id
        self.type_ = type_
        self.parameters = parameters

    def reprJSON(self):
        return {"node": self.__class__.__name__, "function identifier": self.func_id, "type": self.type_, "parameters": self.parameters}


class VariableDeclarationNode(DeclarationNode):
    def __init__(self, line: int, column: int, var_id: str, type_: TypeNode) -> None:
        super().__init__(line, column)
        assert isinstance(type_, TypeNode)
        self.var_id = var_id
        self.type_ = type_

    def reprJSON(self):
        return {"node": self.__class__.__name__, "variable identifier": self.var_id, "type": self.type_}

# Statements


class StmtNode(Node):
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)

    @abstractmethod
    def reprJSON(self):
        pass


class BlockNode(Node):
    def __init__(self, line: int, column: int, statements: List[StmtNode]) -> None:
        super().__init__(line, column)
        assert all(isinstance(n, StmtNode) for n in statements)
        self.statements = statements

    def reprJSON(self):
        return {"node": self.__class__.__name__, "statements": self.statements}


class LocalVariableDeclarationNode(StmtNode):
    def __init__(self, line: int, column: int, var_id: IdentifierExprNode, type_: TypeNode) -> None:
        super().__init__(line, column)
        assert isinstance(type_, TypeNode)
        self.var_id = var_id
        self.type_ = type_

    def reprJSON(self):
        return {"node": self.__class__.__name__, "variable identifier": self.var_id, "type": self.type_}


class VariableAssignmentStmtNode(StmtNode):
    def __init__(self, line: int, column: int, var_id: IdentifierExprNode, expr: ExprNode) -> None:
        super().__init__(line, column)
        assert isinstance(expr, ExprNode)
        self.var_id = var_id
        self.expr = expr

    def reprJSON(self):
        return {"node": self.__class__.__name__, "variable identifier": self.var_id, "expression": self.expr}


class ExprStmtNode(StmtNode):
    def __init__(self, line: int, column: int, expr: ExprNode) -> None:
        super().__init__(line, column)
        assert isinstance(expr, ExprNode)
        self.expr = expr

    def reprJSON(self):
        return {"node": self.__class__.__name__, "expression": self.expr}


class ReturnStmtNode(StmtNode):
    def __init__(self, line: int, column: int, return_expr: ExprNode) -> None:
        super().__init__(line, column)
        assert isinstance(return_expr, ExprNode)
        self.return_expr = return_expr

    def reprJSON(self):
        return {"node": self.__class__.__name__, "return expression": self.return_expr}

# If Statments without else block have it set to None


class IfStmtNode(StmtNode):
    def __init__(self, line: int, column: int, conditional: ExprNode, then_block: BlockNode, else_block: BlockNode or None) -> None:
        super().__init__(line, column)
        assert isinstance(conditional, ExprNode)
        self.conditional = conditional
        self.then_block = then_block
        if else_block is not None:
            assert isinstance(else_block, BlockNode)
            self.else_block = else_block
        else:
            self.else_block = None

    def reprJSON(self):
        return {"node": self.__class__.__name__, "conditional": self.conditional, "then block": self.then_block, "else block": self.else_block}


class WhileStmtNode(StmtNode):
    def __init__(self, line: int, column: int, guard: ExprNode, do_block: BlockNode) -> None:
        super().__init__(line, column)
        assert isinstance(guard, ExprNode)
        assert isinstance(do_block, BlockNode)
        self.guard = guard
        self.do_block = do_block

    def reprJSON(self):
        return {"node": self.__class__.__name__, "guard": self.guard, "do block": self.do_block}


class LocalValueDefinitionNode(StmtNode):
    def __init__(self, line: int, column: int, var_id: IdentifierExprNode, type_: TypeNode, expr: ExprNode) -> None:
        super().__init__(line, column)
        assert isinstance(type_, TypeNode)
        assert isinstance(expr, ExprNode)
        self.var_id = var_id
        self.type_ = type_
        self.expr = expr

    def reprJSON(self):
        return {"node": self.__class__.__name__, "variable identifier": self.var_id, "type": self.type_, "expression": self.expr}

# Definitions


class DefinitionNode(Node):
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)

    @abstractmethod
    def reprJSON(self):
        pass


class FunctionDefinitionNode(DefinitionNode):
    def __init__(self, line: int, column: int, func_id: IdentifierExprNode, type_: TypeNode, parameters: List[Tuple[IdentifierExprNode, TypeNode]], body: BlockNode) -> None:
        super().__init__(line, column)
        assert isinstance(type_, TypeNode)
        assert isinstance(body, BlockNode)
        self.func_id = func_id
        self.type_ = type_
        self.parameters = parameters
        self.body = body

    def reprJSON(self):
        return {"node": self.__class__.__name__, "function identifier": self.func_id, "type": self.type_, "parameters": self.parameters, "body": self.body}


class ValueDefinitionNode(DefinitionNode):
    def __init__(self, line: int, column: int, var_id: IdentifierExprNode, type_: TypeNode, expr: ExprNode) -> None:
        super().__init__(line, column)
        assert isinstance(type_, TypeNode)
        assert isinstance(expr, ExprNode)
        self.var_id = var_id
        self.type_ = type_
        self.expr = expr

    def reprJSON(self):
        return {"node": self.__class__.__name__, "variable identifier": self.var_id, "type": self.type_, "expression": self.expr}

class ArrayDefinitionNode(DefinitionNode):
    def __init__(self, line: int, column: int, array_id : IdentifierExprNode, type_ : TypeNode, items: List[ExprNode]) -> None:
        super().__init__(line, column)
        assert isinstance(type_, TypeNode)
        assert isinstance(array_id, IdentifierExprNode)
        assert all(isinstance(n, ExprNode) for n in items)
        self.array_id = array_id
        self.type_ = type_
        self.items = items

    def reprJSON(self):
        return {"node": self.__class__.__name__, "array identifier": self.array_id, "type": self.type_, "items" : self.items}

# Program


class ProgramNode(Node):
    def __init__(self, line: int, column: int, program_body: List[DeclarationNode or DefinitionNode], main: FunctionDefinitionNode) -> None:
        super().__init__(line, column)
        assert all((isinstance(n, DeclarationNode) or isinstance(
            n, DefinitionNode) for n in program_body))
        self.program_body = program_body
        assert isinstance(main, FunctionDefinitionNode)
        assert main.func_id.identifier == "main", "Last function definition must be main"
        self.main = main

    def reprJSON(self):
        return {"node": self.__class__.__name__, "program body": self.program_body, "main function": self.main}
