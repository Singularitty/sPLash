from dataclasses import dataclass
from enum import Enum


class TypeName(str, Enum):
    DOUBLE = 1
    INT = 2
    STRING = 3
    VOID = 4


class Refinement:
    pass


@dataclass
class ArrayType(str):
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

class TypeError(Exception):
    pass
