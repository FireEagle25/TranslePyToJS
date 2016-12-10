from Lexer.LexError import LexError

from Lexer import LexType


class Lex:

    def __init__(self, lex_type=None, content=None, line=None, pos=None):

        self.type = lex_type
        self.set_content(content)
        self.line = line
        self.pos = pos

    def set_content(self, content):
        if not self.type == "string":
            self.content = content
        else:
            self.content = content[1:len(content) -1]

    def change(self, content):
        self.type = LexType.get_type(content)
        self.set_content(content)

    def print(self):
        self.check()
        print(self)

    def check(self):
        if self.type is not None:

            if self.type == "string_start":
                raise LexError("Ожидалось завершение строки, " + str(self.line))

            elif self.type == "float_start":
                raise LexError("Ожидалось завершение числа с точкой, " + str(self.line))

            elif self.type == "space":
                pass
            else:
                return
        else:
            raise LexError("Ошибка, недопустимый символ, " + str(self.line))
    def __str__(self):
        return self.content + "|" + self.type + "|line:" + str(self.line) + "|lex_pos:" + str(self.pos)