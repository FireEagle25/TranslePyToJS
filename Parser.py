class Parser:

    def __init__(self, lexs):
        self.lexs = lexs
        self.curr_lex_num = 1
        self.get_next_lex()

    def get_lex(self, shift):
        return self.lexs[self.curr_lex_num + shift]

    def get_next_lex(self):
        self.curr_lex_num += 1
        self.curr_lex = self.lexs[self.curr_lex_num]


    # EXPRESSIONS


    # mutual method
    def expression(self, shift, content_variants=[], lex_type=None):

        lex = self.get_lex(shift)

        if lex.type == lex_type:
            for variant in content_variants:
                if lex.content == variant:
                    # Todo: добавить в дерево
                    return True
        return False

    def plus_ex(self, shift):
        return self.expression(shift, ["+"], "alg_ops")

    def if_ex(self, shift):
        return self.expression(shift, ["if"], "words")

    def while_ex(self, shift):
        return self.expression(shift, ["while"], "words")

    def double_dot_ex(self, shift):
        return self.expression(shift, [":"], "spec_symbols")

    def assignment_op_ex(self, shift):
        return self.expression(shift, ["="], "alg_ops")

    def elif_ex(self, shift):
        return self.expression(shift, ["elif"], "words")

    def else_ex(self, shift):
        return self.expression(shift, ["else"], "words")

    def closing_bracket_ex(self, shift):
        return self.expression(shift, [")"], "brackets")

    def opening_bracket_ex(self, shift):
        return self.expression(shift, ["("], "brackets")

    def bool_op_not_ex(self, shift):
        return self.expression(shift, ["not"], "bool_op")

    def comp_op(self, shift):
        return self.expression(shift, ["<", ">", ">=", "<=", "=="], "comp_op")

    def augassign_ex(self, shift):
        return self.expression(shift, ["+=", "-=", "*=", "/="], "alg_ops")

    def tab_ex(self, shift):
        return self.expression(shift, ["\t"], "spec_symbols")



    #SIMPLE TYPES AND VARS


    #mutual method
    def type_or_var(self, shift, lex_type):
        return self.get_lex(shift).type == lex_type

    def float(self, shift):
        return self.type_or_var(shift,"float_num")

    def int(self, shift):
        return self.type_or_var(shift,"num")

    def string(self, shift):
        return self.type_or_var(shift,"string")

    def var_name(self, shift):
        return self.type_or_var(shift,"var_name")


    #COMPLEX SENTENCES


    def bool(self, shift):
        pass