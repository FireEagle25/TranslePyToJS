from Lexer.Lex import Lex


class Parser:

    #TODO: для каждого возвращаемого False прописать тип ошибки

    def __init__(self, lexs):
        self.lexs = lexs
        a = self.expr(0)
        print(a)

    def get_lex(self, shift):

        if len(self.lexs) <= shift:
            return Lex()

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
        if operation(shift):
            return general_method(shift + 1)
        else:
            return shift

    def object_in_brackets(self, shift, general_method):
        #TODO: ошибки в аргументах
        if self.opening_bracket_ex(shift):
            shift1 = general_method(shift + 1)
            if shift1:
                if self.closing_bracket_ex(shift1):
                    return shift1 + 1
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
                num_op_num = self.num_op_num(num_in_brackets)
                return num_op_num if num_op_num else num_in_brackets
            else:
                return False

    def num_in_brackets(self, shift):
        return self.object_in_brackets(shift, self.num)

    def num_op_num(self, shift):
        return self.operation_with_object(shift, self.arithmetic_operation, self.num)


    #bool

    def bool(self, shift):

        if self.bool_op_not_ex(shift):
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
            return self.bool_op_bool(bool_in_brackets)
        elif num:
            if self.comp_op(num):
                bool_length_variants.append(self.bool_op_bool(self.num(num + 1)))

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
                return self.str_op_str(str_in_brackets)
            else:
                return False

    def str_op_str(self, shift):
        return self.operation_with_object(shift, self.plus_ex, self.string)

    def str_in_brackets(self, shift):
        return self.object_in_brackets(shift, self.string)


    #term

    def term(self, shift):

        str_item = self.string(shift)
        num_item = self.num(shift)
        bool_item = self.bool(shift)

        max_term = max([str_item, num_item, bool_item])

        return max_term


    #id_with_assignment_op

    def id_with_assignment_op(self, shift):

        if self.var_name(shift):
            if self.assignment_op_ex(shift + 1):
                return shift + 2
            else:
                return False
        else:
            return False

    #expr

    def expr(self, shift):
        id_with_assignment_op = self.id_with_assignment_op(shift)
        term = self.term(shift)

        if id_with_assignment_op:
            inserted_term = self.term(id_with_assignment_op)
            if inserted_term:
                return inserted_term

        if term:
            return term

        return False