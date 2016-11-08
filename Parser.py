class Parser:

    def __init__(self, lexs):
        self.lexs = lexs
        self.curr_lex_num = 0
        self.curr_lex = lexs[0]

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

    def arithmetic_operation(self, shift):
        return self.expression(shift, ["+", "-", "*", "/"], "alg_ops")

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


    #num

    def num(self, shift):

        if self.int(shift) or self.float(shift) or self.var_name(shift):
            print("чиселко")
            num_op_num = self.num_op_num(shift + 1)
            if num_op_num:
                return num_op_num
            else:
                print("чиселко")
                return shift + 1
        else:
            b_num = self.num_in_brackets(shift)
            if b_num:
                return self.num_op_num(b_num + 1)
            else:
                return "Ожидалось арифм. выражение"

    def num_in_brackets(self, shift):

        if self.opening_bracket_ex(shift):
            print("открыли скобочку")
            shift1 = self.num(shift + 1)
            if shift1:
                if self.closing_bracket_ex(shift1):
                    print("закрыли скобку")
                    return shift1
                else:
                    print("Ожидалось закрытие скобки")
                    exit()
            else:
                print("Ожидалось логическое выражение")
                exit()

    def num_op_num(self, shift):

        if len(self.lexs) < shift + 2 or self.get_lex(shift).line != self.get_lex(shift + 1).line:
            return shift

        if self.arithmetic_operation(shift):
            print("плюсик")
            return self.num(shift + 1)

        return shift