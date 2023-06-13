from dataclasses import dataclass
from enum import Enum

class TypeName(str, Enum):
    DOUBLE = "Double"
    INT = "Int"
    STRING = "String"
    VOID = "Void"

    def __str__(self) -> str:
        if self.value == TypeName.DOUBLE:
            return "Double"
        if self.value == TypeName.INT:
            return "Int"
        if self.value == TypeName.STRING:
            return "String"
        if self.value == TypeName.VOID:
            return "Void"

@dataclass
class ArrayType():
    type_name: TypeName
    nest_level: int

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, ArrayType):
            return False
        if self.type_name != __value.type_name:
            return False
        if self.nest_level != __value.nest_level:
            return False
        return True

    def __str__(self) -> str:
        return "["*self.nest_level + self.type_name + "]"*self.nest_level

    def element_type(self):
        if self.nest_level == 1:
            return self.type_name
        return ArrayType(self.type_name, self.nest_level-1)

class TypeError(Exception):
    pass

class LiquidType:
    
    def __init__(self, var: str, ttype: TypeName or ArrayType, refinement = None):
        self.var = var
        self.ttype = ttype
        self.refinement = refinement
        
    def is_refined(self) -> bool:
        return self.refinement is not None
    
    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, LiquidType):
            return False
        if self.ttype != __value.ttype:
            return False
        if self.refinement != __value.refinement:
            return False
        return True
    
    def __str__(self) -> str:
        if self.is_refined():
            return "{" + f"{self.var}: {self.ttype} | {self.refinement}" + "}"
        else:
            return str(self.ttype)