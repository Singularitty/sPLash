import sys
from typing import List, Tuple, Any
from lark import Lark, Transformer
from AstTransformer import AstTransformer
import rich

def main():

    program_file = sys.argv[1]

    program = None

    with open(program_file, "r") as infile:
        program = infile.read()

    parser = Lark.open("sPLash.lark")

    tree = parser.parse(program)

    print(AstTransformer().transform(tree))

    rich.print(tree)

if __name__ == "__main__":
    main()