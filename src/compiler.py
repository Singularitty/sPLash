import sys
import json
from lark import Lark
from parser.ast_transformer import AstTransformer
from parser.ast_nodes import ComplexEncoder
from typechecker.typechecker import *
from codegenerator.codegen import compile

LARK_FILE_PATH = "src/parser/sPLash.lark"

def main():

    program = None

    print_ast = False

    # file_path should always be last argument of argv
    file_path = sys.argv[-1]

    # splash bash script ignores extra arguments, so no need to check for other cases
    if len(sys.argv) == 3 and sys.argv[1] == "--tree":
        print_ast = True

    
    # handle file related exceptions
    try:
        with open(file_path, "r") as infile:
            program = infile.read()
    except FileNotFoundError:
        print("Error: File not found")
        sys.exit(2)
    except:
        print("Error: Couldn't open file")
        sys.exit(3)


    # initiate parser with sPLash grammar
    parser = Lark.open(LARK_FILE_PATH)
    
    # parse program
    try:
        tree = parser.parse(program)
    except Exception as e:
        print(e)
        sys.exit(1)
        

    # create ast
    ast: ProgramNode = AstTransformer().transform(tree)

    # print ast in JSON format
    if print_ast:
        print(json.dumps(ast, cls=ComplexEncoder, indent=2))
    else:

        # Type check
        try:
            tp = TypeChecker(ast)
        except TypeError as err:
            raise sys.exit(err)

        if not tp.valid:
            print("Type Checking Failed!\nErrors:")
            for err in tp.errors:
                print(err)
            sys.exit(4)
        
        try:
            llvm = compile(ast)
            with open(file_path[:-2] + "ll", "w") as llvm_out:
                llvm_out.write(llvm)
        except IOError as e:
            print(e)
            sys.exit(3)


if __name__ == "__main__":
    main()