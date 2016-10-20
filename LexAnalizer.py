import re
import LexType


class Lexer:

    def __init__(self, filename):
        self.work = True
        self.file = open(filename, 'r')
        self.ch = self.file.read(1)

        self.line = 1
        self.char_num_in_line = 1
        self.lex = None
        self.lex_type = None

    def next_ch(self):
        self.ch = self.file.read(1)

    def print_lex(self):
        if self.lex_type == 12:
            print("Ошибка, там строка не правильно написана, исправь, неуч!")
            self.work = False
        elif self.lex_type == 13:
            print("Ошибка, там, это, флоат кривой")
            self.work = False
        elif self.lex_type == 11:
            pass
        elif self.lex_type == 9:
            print(self.lex[1:len(self.lex) -1] + "|" + self.lex_type + "|line:" + str(self.line) + "|lex_pos:" + str(self.char_num_in_line))
        elif self.lex_type is not None:
            print(self.lex + "|" + self.lex_type + "|line:" + str(self.line) + "|lex_pos:" + str(self.char_num_in_line))
        else:
            print("Ошибка, недопустимый символ")
            self.work = False

        self.char_num_in_line += len(self.lex)
        self.lex = ""
        self.lex_type = None

    def check_new_line(self):
        if self.ch == '\n':
            self.print_lex()
            self.next_ch()
            self.line += 1
            self.char_num_in_line = 1
            return True
        else:
            return False

    def lex_analize(self):

        while self.ch:

            if not self.work:
                break

            if self.check_new_line():
                pass

            lex_candidate = self.ch
            if self.lex is not None:
                lex_candidate = self.lex + self.ch

            new_lex_type = LexType.get_type(lex_candidate)

            if not new_lex_type:
                self.print_lex()
                self.char_num_in_line += len(self.lex)
                self.lex = ""
                self.lex_type = None
            else:
                self.next_ch()
                self.lex = lex_candidate
                self.lex_type = new_lex_type

lexer = Lexer("1.txt")
lexer.lex_analize()
