import re


class Lexer:
    lex_types = ["words", "bool_ops", "bools", "alg_ops", "comp_op", "brackets", "spec_symbols", "num", "float_num",
                 "string", "var_name", "space", "string_start", "float_start"]

    lexs_regex = {

        0: [re.compile('^if$'), re.compile('^while$'), re.compile('^else$'),
            re.compile('^elif$')],

        1: [re.compile('^and$'), re.compile('^or$'), re.compile('^not$')],

        2: [re.compile('^True$'), re.compile('^False')],

        3: [re.compile('^\+$'), re.compile('^-$'), re.compile('^\*$'), re.compile('^\+=$'), re.compile('^-=$'),
            re.compile('^\*=$'), re.compile('^=$')],

        4: [re.compile('^<$'), re.compile('^>$'), re.compile('^<=$'), re.compile('^>=$'), re.compile('^==$')],

        5: [re.compile('^\($'), re.compile('^\)$')],

        6: [re.compile('^:$'), re.compile('^\t$')],

        7: [re.compile('^[0-9]+$')],
        8: [re.compile('^\d+\.\d+$')],

        9: [re.compile('^".*"$')],

        10: [re.compile('^[a-zA-Z_]+[a-zA-Z0-9]*$')],

        11: [re.compile('^\s?$')],

        12: [re.compile('^".*')],

        13: [re.compile('^\d+\.$')]
    }

    def __init__(self, filename):
        self.isWork = True
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
            self.isWork = False
        elif self.lex_type == 13:
            print("Ошибка, там, это, флоат кривой")
            self.isWork = False
        elif self.lex_type == 11:
            pass
        elif self.lex_type == 9:
            print(self.lex[1:len(self.lex) -1] + "|" + Lexer.lex_types[self.lex_type] + "|line:" + str(self.line) + "|lex_pos:" + str(self.char_num_in_line))
        elif self.lex_type is not None:
            print(self.lex + "|" + Lexer.lex_types[self.lex_type] + "|line:" + str(self.line) + "|lex_pos:" + str(self.char_num_in_line))
        else:
            print("Ошибка, недопустимый символ")
            self.isWork = False

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

            if not self.isWork:
                break

            if self.check_new_line():
                pass

            lex_candidate = self.ch
            if self.lex is not None:
                lex_candidate = self.lex + self.ch

            continue_old_lex = False

            for i in range(len(Lexer.lexs_regex)):
                for lex_type in Lexer.lexs_regex[i]:
                    if re.match(lex_type, lex_candidate) and not continue_old_lex:
                        self.lex = lex_candidate
                        self.lex_type = i
                        continue_old_lex = True

            if not continue_old_lex:
                self.print_lex()
            else:
                self.next_ch()

lexer = Lexer("1.txt")
lexer.lex_analize()
