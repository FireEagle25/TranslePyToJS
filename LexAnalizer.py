import LexType
from Lex import Lex


class Lexer:
    def __init__(self, filename):
        self.filename = filename
        self.clear()

    def __new_lex__(self):
        self.lex = Lex(line=self.line, pos=self.ch_pos)

    def __next_ch__(self):
        self.ch = self.file.read(1)
        self.ch_pos += 1

    def __check_new_line__(self):

        if self.ch == '\n':
            self.line += 1
            self.ch_pos = 1
            if self.lex.content:
                self.lexs.append(self.lex)
                self.lex.print()
            self.__new_lex__()
            self.__next_ch__()
            return True

        return False

    def clear(self):
        self.work = True
        self.file = open(self.filename, 'r')
        self.ch_pos = 0
        self.line = 1

        self.__next_ch__()
        self.__new_lex__()
        self.lexs = []

    def lex_analize(self):

        while self.ch:

            if not self.work:
                break

            if self.__check_new_line__():
                continue

            lex_bidder = self.lex.content + self.ch if self.lex.content else self.ch

            lex_type = LexType.get_type(lex_bidder)

            if lex_type:
                self.__next_ch__()
                self.lex.change(lex_bidder)
            else:
                self.lex.print()
                self.lexs.append(self.lex)
                self.__new_lex__()

        return self.lexs


lexer = Lexer("1.txt")
lexer.lex_analize()