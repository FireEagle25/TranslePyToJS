import LexType


class Lex:

    def __init__(self, lex_type=None, content=None, line=None, pos=None):

        self.type = lex_type
        self.content = content

        if not self.type == "string":
            self.content = content
        else:
            self.content = content[1:len(content) -1]
        self.line = line
        self.pos = pos

    def change(self, content):
        self.type = LexType.get_type(content)
        self.content = content

    def print(self):

        if self.type is not None:

            if self.type == "string_start":
                print("Ожидалось завершение строки.")
                return False

            elif self.type == "float_start":
                print("Ожидалось завершение числа с точкой.")
                return False

            elif self.type == "space":
                return True

            else:
                print(self)
                return True
        else:
            print("Ошибка, недопустимый символ")
            return False

    def __str__(self):
        return self.content + "|" + self.type + "|line:" + str(self.line) + "|lex_pos:" + str(self.pos)