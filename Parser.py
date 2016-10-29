class Parser:

    def __init__(self, lexs):
        self.lexs = lexs
        self.curr_lex_num = 1
        self.get_next_lex()

    def get_next_lex(self):
        self.curr_lex_num += 1
        self.curr_lex = self.lexs[self.curr_lex_num]

    def expression(self, content_variants, type):
        if self.curr_lex.type == type:
            for variant in content_variants:
                if self.curr_lex.content == variant:
                    # Todo: добавить в дерево
                    self.get_next_lex()
                    return True
        return False

    def plus_ex(self):
        return self.expression(["+"], "alg_ops")

    def if_ex(self):
        return self.expression(["if"], "words")

    def while_ex(self):
        return self.expression(["while"], "words")

    def double_dot(self):
        return self.expression([":"], "spec_symbols")

    def assignment_op(self):
        return self.expression(["="], "alg_ops")

    def elif_ex(self):
        return self.expression(["elif"], "words")

    def else_ex(self):
        return self.expression(["else"], "words")

    def closing_bracket(self):
        return self.expression([")"], "brackets")

    def opening_bracket(self):
        return self.expression(["("], "brackets")

    def bool_op_not(self):
        return self.expression(["not"], "bool_op")

    def comp_op(self):
        return self.expression(["<", ">", ">=", "<=", "=="], "comp_op")

    def augassign(self):
        return self.expression(["+=", "-=", "*=", "/="], "alg_ops")

    def line_end(self):
        #TODO: исправить хуету
        if self.curr_lex.line != self.lexs[self.curr_lex_num + 1]:
            return True
        return False

    def tab(self):
        return self.expression(["\t"], "spec_symbols")

    def float(self):
        if self.curr_lex.type == "float_num":
            #TODO: Э, я не помню, что я тут хотел написать
            return True

        return False

    def int(self):
        if self.curr_lex.type == "float_num":
            #TODO: Э, я не помню, что я тут хотел написать
            return True

        return False