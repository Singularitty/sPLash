from dataclasses import dataclass
from enum import Enum

class TypeName(str, Enum):
    DOUBLE = "Double"
    INT = "Int"
    STRING = "String"
    VOID = "Void"

class Refinement:
    pass


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
