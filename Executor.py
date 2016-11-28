from Lexer.LexAnalizer import Lexer
from Parser.Parser import Parser


def main(argv=None):
    file_name = "1.txt"
    lexs = Lexer(file_name).lex_analize()
    tree = Parser(lexs).parse()
    print(tree)

if __name__ == "__main__":
    main()