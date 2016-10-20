import LexType
from Lex import Lex


class Lexer:

    def __init__(self, filename):
        self.work = True
        self.file = open(filename, 'r')
        self.ch_pos = 0
        self.line = 1
        self.next_ch()
        self.new_lex()

    def new_lex(self):
        self.lex = Lex(line=self.line, pos=self.ch_pos)

    def next_ch(self):
        self.ch = self.file.read(1)
        self.ch_pos += 1

    def print_lex(self):
        self.work = self.lex.print()

    def check_new_line(self):

        if self.ch == '\n':
            self.next_ch()
            self.line += 1
            self.ch_pos = 1
            return True

        return False

    def lex_analize(self):

        while self.ch:

            if not self.work:
                break

            if self.check_new_line():
                continue

            lex_bidder = self.lex.content + self.ch if self.lex.content else self.ch

            lex_type = LexType.get_type(lex_bidder)

            if lex_type:
                self.next_ch()
                self.lex.change(lex_bidder)
            else:
                self.print_lex()
                self.new_lex()


lexer = Lexer("1.txt")
lexer.lex_analize()
