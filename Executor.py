import sys

from Lexer.LexAnalizer import Lexer as l
from Parser.Parser import Parser as p
from SemanticAnalizer.SemanticAnalizer import SemanticAnalizer as sa
from CodeGenerator.CodeGenerator import CodeGenerator as cg


def translate(input, output):

    lexs = l(input).lex_analize()

    tree = p(lexs).parse()
    sa(tree).anilize()

    cg(tree).write_code_to_file(output)




def main():

    if len(sys.argv) < 3:
        print("Необходимо ввести два имени файла: входной и выходной")
        exit()

    translate(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()
