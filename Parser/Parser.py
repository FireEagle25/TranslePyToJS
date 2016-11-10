import Tools.Sorter

class Parser:

    def __init__(self, lexs):
        self.lexs = lexs
        a = self.term(0)

    def get_lex(self, shift):
        return self.lexs[shift]


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

    def bool_operation(self, shift):
        return self.expression(shift, ["and", "or"], "bool_op")

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

    def string_const(self, shift):
        return self.type_or_var(shift,"string")

    def var_name(self, shift):
        return self.type_or_var(shift,"var_name")

    def bool_const(self, shift):
        return self.type_or_var(shift, "bools")



    #COMPLEX SENTENCES

    # mutual methods

    def operation_with_object(self, shift, operation, general_method):

        if len(self.lexs) < shift + 2 or self.get_lex(shift).line != self.get_lex(shift + 1).line:
            return shift

        if operation(shift):
            #print("+")
            return general_method(shift + 1)

        return shift

    def object_in_brackets(self, shift, general_method):
        #TODO: ошибки в аргументах
        if self.opening_bracket_ex(shift):
            #print("(")
            shift1 = general_method(shift + 1)
            if shift1:
                if self.closing_bracket_ex(shift1):
                    #print(")")
                    return shift1
                else:
                    #TODO вывод ошибки
                    return False
            else:
                # TODO вывод ошибки
                return False


    #num

    def num(self, shift):

        if self.int(shift) or self.float(shift) or self.var_name(shift):
            num_op_num = self.num_op_num(shift + 1)
            if num_op_num:
                return num_op_num
            else:
                return shift + 1
        else:
            num_in_brackets = self.num_in_brackets(shift)
            if num_in_brackets:
                return self.num_op_num(num_in_brackets + 1)
            else:
                return False

    def num_in_brackets(self, shift):
        return self.object_in_brackets(shift, self.num)

    def num_op_num(self, shift):
        return self.operation_with_object(shift, self.arithmetic_operation, self.num)


    #bool

    def bool(self, shift):

        if self.bool_op_not_ex(shift):
            print("not")
            return self.bool(shift + 1)

        bool_length_variants = []

        if self.bool_const(shift) or self.var_name(shift):

            bool_op_bool = self.bool_op_bool(shift + 1)

            if bool_op_bool:
                bool_length_variants.append(bool_op_bool)
            else:
                bool_length_variants.append(shift + 1)

        bool_in_brackets = self.bool_in_brackets(shift)

        num = self.num(shift)

        if bool_in_brackets:
            return self.bool_op_bool(bool_in_brackets + 1)
        elif num:
            if len(self.lexs) >= num + 2:
                if self.get_lex(shift).line != self.get_lex(shift + 1).line and self.comp_op(num):
                    bool_length_variants.append(self.num(num + 1))

        if len(bool_length_variants) > 0:
            return max(bool_length_variants)

        return False

    def bool_in_brackets(self, shift):
        return self.object_in_brackets(shift, self.bool)

    def bool_op_bool(self, shift):
        return self.operation_with_object(shift, self.bool_operation, self.bool)


    #string

    def string(self, shift):
        if self.string_const(shift) or self.var_name(shift):
            str_op_str = self.str_op_str(shift + 1)
            if str_op_str:
                return str_op_str
            else:
                return shift + 1
        else:
            str_in_brackets = self.str_in_brackets(shift)
            if str_in_brackets:
                return self.str_op_str(str_in_brackets + 1)
            else:
                return False

    def str_op_str(self, shift):
        return self.operation_with_object(shift, self.plus_ex, self.string)

    def str_in_brackets(self, shift):
        return self.object_in_brackets(shift, self.string)


    #term

    def term(self, shift):

        str_item = ["str", self.string(shift)]
        num_item = ["num", self.num(shift)]
        bool_item = ["bool", self.bool(shift)]

        max_term = Tools.Sorter.get_max([str_item, num_item, bool_item])

        print(max_term)
        return max_term
