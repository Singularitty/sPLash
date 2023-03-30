import sys

from lark import Lark, Transformer





def main():

    program_file = sys.argv[1]

    program = None

    with open(program_file, "r") as infile:
        program = infile.read()

    parser = Lark.open("sPLash.lark")

    print(parser.parse(program).pretty())



if __name__ == "__main__":
    main()