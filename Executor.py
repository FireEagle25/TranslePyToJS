from Lexer.LexAnalizer import Lexer
from Parser.Parser import Parser
from  Parser.SemanticAnalizer import SemanticAnalizer

def translate(filename):
    file_name = filename
    lexs = Lexer(file_name).lex_analize()
    tree = Parser(lexs).parse()
    print(tree)
    sem_an = SemanticAnalizer(tree).start_anilize()

def main(argv=None):
    translate("1.txt")

if __name__ == "__main__":
    main()