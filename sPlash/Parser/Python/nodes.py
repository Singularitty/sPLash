from abc import ABC
from typing import List

class Node(ABC):

    def __init__(self, line: int, column: int) -> None:
        self.line = line
        self.column = column

class ProgramNode(Node):
    pass

class DeclarationNode(Node):
    pass

class DefinitionNode(Node):
    pass

class BlockNode(Node):
    pass




class StmtNode(Node):
    def __init__(self, line: int, column: int) -> None:
        super().__init__(line, column)

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
        self.sign = sign

class FloatLiteralExprNode(ExprNode):
    def __init__(self, line: int, column: int, value: float) -> None:
        super().__init__(line, column)
        self.value = value

class SignedFloatLiteralExprNode(FloatLiteralExprNode):
    def __init__(self, line: int, column: int, value: float, sign: str) -> None:
        super().__init__(line, column, value)
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
        self.func_name = func_id
        self.args = args

class ArithmeticExprNode(ExprNode):
    def __init__(self, line: int, column: int):
        pass