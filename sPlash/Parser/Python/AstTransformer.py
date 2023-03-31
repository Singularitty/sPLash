from lark import Lark, Transformer
from nodes import *
from typing import List, Tuple, Any

class AstTransformer(Transformer):

    def ID(self, value) -> IdentifierExprNode:
        return IdentifierExprNode()

    def FLOATLIT(self, value):
        return float(value)

    def SIGNED_FLOATLIT(self, value):
        return float(value)
    
    def INTLIT(self, value):
        return int(value)

    def SIGNED_INT(self, value):
        print(value)
        return int(value)

    def STRING(self, value):
        return value

    def true(self, value):
        if value == "true":
            return True
        else:
            raise Exception

    def false(self, value):
        if value == "false":
            return False
        else:
            raise Exception

    def block(self, s):
        pass

    def value_def(self, s):
        pass

    