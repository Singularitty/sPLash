import sys
import json
from lark import Lark
from parser.ast_transformer import AstTransformer
from parser.ast_nodes import ComplexEncoder

LARK_FILE_PATH = "src/parser/sPLash.lark"

def main():

    program = None

    print_ast = False

    # file_path should always be last argument of argv
    file_path = sys.argv[-1]

    # splash bash script never ignores extra arguments, so no need to check for other cases
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
    tree = parser.parse(program)

    # create ast
    ast = AstTransformer().transform(tree)

    # print ast in JSON format
    if print_ast:
        print(json.dumps(ast, cls=ComplexEncoder, indent=2))

if __name__ == "__main__":
    main()
