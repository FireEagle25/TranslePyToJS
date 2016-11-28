from Lexer.Lex import Lex
from treelib import Node, Tree

class Parser:

    #TODO: для каждого возвращаемого False прописать тип ошибки

    def __init__(self, lexs):

        self.lexs = lexs
        self.clear()

    def parse(self):
        self.clear()

        program = self.program()
        self.tree = program[0]
        return self.tree

    def clear(self):
        self.uniq_postfix = 0
        self.tree = None
        self.lattest_lex_num = 0

    def get_lex(self, shift):

        if len(self.lexs) <= shift:
            return Lex()
        elif shift > self.lattest_lex_num:
            self.lattest_lex_num = shift

        return self.lexs[shift]

    def get_uniq_postfix(self):

        self.uniq_postfix += 1
        return str(self.uniq_postfix)

    # EXPRESSIONS


    # mutual method
    def expression(self, shift, content_variants=[], lex_type=None):

        lex = self.get_lex(shift)

        if lex.type == lex_type:

            for variant in content_variants:
                if lex.content == variant:
                    tree = Tree()
                    tree.create_node(tag=self.get_lex(shift).content, data=shift)
                    return tree, True

        return None, False, "Ожидалось " + lex_type

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

        tree = None
        type_equality = self.get_lex(shift).type == lex_type

        if type_equality:
            tree = Tree()
            tree.create_node(self.get_lex(shift).content, "type_or_var" + self.get_uniq_postfix(), data=shift)

        return tree, type_equality, shift + 1

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

    def operation_with_object(self, shift, operation, general_method, node_name="op_with_obj"):

        op_res = operation(shift)
        tree = None
        returned_shift = shift
        if op_res[1]:
            gen_method_res = general_method(shift + 1)
            if gen_method_res[1]:
                tree = Tree()
                node_id = node_name + self.get_uniq_postfix()
                tree.create_node(node_name, node_id)
                tree.create_node(tag=self.get_lex(shift).content, parent=node_id, data=shift)
                tree.paste(node_id, gen_method_res[0])
                returned_shift = gen_method_res[2]
            else:
                print("Ожидался второй опперанд")
                print("После "+str(self.get_lex(shift)))
                exit()

        return tree, tree is not None, returned_shift

    def object_in_brackets(self, shift, general_method, node_name="obj_in_brackets"):

        tree = None
        bracket = self.opening_bracket_ex(shift)
        if bracket[1]:
            gen_method_res = general_method(shift + 1)
            if gen_method_res[1]:
                closing_bracket = self.closing_bracket_ex(gen_method_res[2])
                if closing_bracket[1]:
                    tree = Tree()
                    node_id = node_name + self.get_uniq_postfix()
                    tree.create_node(node_name, node_id)
                    tree.paste(node_id, gen_method_res[0])

                    return tree, True, gen_method_res[2] + 1
                else:
                    print("Ожидалась закрывающая скобка")
                    print("После " + str(self.get_lex(gen_method_res[2] - 1)))
                    exit()
            else:
                print("Ожидалось внутреннее выражение")
                print("После "+str(self.get_lex(shift)))
                exit()
        else:
            return tree, False, "Ожидалась открывающая скобка"

    def word_with_bool(self, shift, tab_count, word_func, node_name="word_with_bool"):

        tree = Tree()
        node_id = node_name + self.get_uniq_postfix()
        tree.create_node(node_name, node_id)

        for i in range(shift, shift + tab_count):
            if not self.tab_ex(i)[1]:
                return tree, False

        word_ex = word_func(shift + tab_count)

        if word_ex[1]:
            bool_statement = self.bool(shift + tab_count + 1)
            if bool_statement[1]:
                double_dot = self.double_dot_ex(bool_statement[2])
                if double_dot[1]:
                    statements = self.statements(bool_statement[2] + 1, tab_count + 1)
                    if statements[1]:
                        tree.paste(node_id, bool_statement[0])
                        tree.paste(node_id, statements[0])
                        return tree, True, statements[2], node_id
                    else:
                        print("Ожидались вложенные блоки")
                        print("После " + str(self.get_lex(bool_statement[2])))
                        exit()
                else:
                    print("Ожадалось двоеточие")
                    print("После " + str(self.get_lex(shift + tab_count)))
                    exit()
            else:
                print("Ожидалось булево выражение")
                print("После " + str(self.get_lex(shift)))
                exit()

        return None, False

    #num

    def num(self, shift):
        tree = None

        int = self.int(shift)
        float = self.float(shift)
        var_name = self.var_name(shift)

        if int[1] or float[1] or var_name[1]:

            tree = Tree()
            node_id = "num" + self.get_uniq_postfix()
            tree.create_node("Num", node_id)

            if int[1]:
                tree.paste(node_id, int[0])
            elif float[1]:
                tree.paste(node_id, float[0])
            elif var_name[1]:
                tree.paste(node_id, var_name[0])

            num_op_num = self.num_op_num(shift + 1)
            if num_op_num[1]:
                tree.paste(node_id, num_op_num[0])
                return tree, True, num_op_num[2]
            else:
                return tree, True, shift + 1
        else:
            num_in_brackets = self.num_in_brackets(shift)
            if num_in_brackets[1]:
                tree = Tree()
                node_id = "num" + self.get_uniq_postfix()
                tree.create_node("Num", node_id)
                tree.paste(node_id, num_in_brackets[0])

                num_op_num = self.num_op_num(num_in_brackets[2])

                if num_op_num[1]:
                    tree.paste(node_id, num_op_num[0])

                return tree, True, num_op_num[2] if num_op_num[1] else num_in_brackets[2]
            else:
                return tree, False, "Ожидалось число"

    def num_in_brackets(self, shift):
        return self.object_in_brackets(shift, self.num, "Number in brackets")

    def num_op_num(self, shift):
        return self.operation_with_object(shift, self.arithmetic_operation, self.num, "Operation with number")

    def compare_nums(self, shift):

        tree = None
        returned_shift = shift
        num1 = self.num(shift)

        if num1[1]:
            comp_op = self.comp_op(num1[2])
            if comp_op[1]:
                num2 = self.num(num1[2] + 1)
                if num2[1]:
                    tree = num1[0]

                    node_id = "comp nums" + self.get_uniq_postfix()
                    tree.create_node("Compare nums", node_id, parent=tree.root)
                    tree.paste(node_id, comp_op[0])
                    tree.paste(node_id, num2[0])

                    returned_shift = num2[2]
                else:
                    return tree, tree is not None, "Ожидалось число"
            else:
                return tree, tree is not None, "Ожидалось Сравнение чисел"

        return tree, tree is not None, returned_shift


    #bool

    def bool(self, shift):

        node_id = "bool" + self.get_uniq_postfix()

        bool_not_op = self.bool_op_not_ex(shift)
        if bool_not_op[1]:
            bool_item = self.bool(shift + 1)
            if bool_item[1]:

                tree = Tree()
                tree.create_node("Bool", node_id)
                tree.create_node(tag="not", parent=node_id, data=shift)
                tree.paste(node_id, bool_item[0])
                return tree, Tree, bool_item[2]

        bool_variants = []

        bool_const = self.bool_const(shift)
        var_name = self.var_name(shift)

        if bool_const[1] or var_name[1]:

            tree = Tree()
            tree.create_node("Bool", node_id)

            if bool_const[1]:
                tree.paste(node_id, bool_const[0])
            elif var_name[1]:
                tree.paste(node_id, var_name[0])

            bool_op_bool = self.bool_op_bool(shift + 1)

            if bool_op_bool[1]:
                tree.paste(node_id, bool_op_bool[0])

            bool_variants.append((tree, bool_op_bool[2] if bool_op_bool[1] else shift + 1))

        bool_in_brackets = self.bool_in_brackets(shift)

        comp_op = self.compare_nums(shift)

        if bool_in_brackets[1]:
            tree = Tree()
            tree.create_node("Bool", node_id)
            tree.paste(node_id, bool_in_brackets[0])

            bool_op_bool = self.bool_op_bool(bool_in_brackets[2])
            if bool_op_bool[1]:
                tree.paste(node_id, bool_op_bool[0])

            return tree, True, bool_in_brackets[2]
        elif comp_op[1]:
            tree = Tree()
            tree.create_node("Bool", node_id)
            tree.paste(node_id, comp_op[0])

            bool_op_bool = self.bool_op_bool(comp_op[2])
            if bool_op_bool[1]:
                tree.paste(node_id, bool_op_bool[0])

            bool_variants.append((tree, bool_op_bool[2] if bool_op_bool[1] else comp_op[2]))

        if len(bool_variants) > 0:
            max = 0
            for i in range(len(bool_variants)):
                if bool_variants[max][1] < bool_variants[i][1]:
                    max = i

            return bool_variants[max][0], True, bool_variants[max][1]

        return None, False, "Ждали буль"

    def bool_in_brackets(self, shift):
        return self.object_in_brackets(shift, self.bool)

    def bool_op_bool(self, shift):
        return self.operation_with_object(shift, self.bool_operation, self.bool)


    #string

    def string(self, shift):
        tree = None
        string_const = self.string_const(shift)
        var_name = self.var_name(shift)
        if string_const[1] or var_name[1]:

            tree = Tree()
            node_id = "String" + self.get_uniq_postfix()
            tree.create_node("String", node_id)

            if string_const[1]:
                tree.paste(node_id, string_const[0])
            elif var_name[1]:
                tree.paste(node_id, var_name[0])

            str_op_str = self.str_op_str(shift + 1)

            if str_op_str[1]:
                tree.paste(node_id, str_op_str[0])
                return tree, True, str_op_str[2]
            else:
                return tree, True, shift + 1
        else:
            str_in_brackets = self.str_in_brackets(shift)
            if str_in_brackets[1]:
                str_op_str = self.str_op_str(str_in_brackets[2])

                tree = Tree()
                node_id = "String" + self.get_uniq_postfix()
                tree.create_node("String", node_id)
                tree.paste(node_id, str_in_brackets[0])

                if str_op_str[1]:
                    tree.paste(node_id, str_op_str[0])

                return tree, True, str_op_str[2] if str_op_str[1] else str_in_brackets[2]
            else:
                return tree, False, "Ждали строку"

    def str_op_str(self, shift):
        return self.operation_with_object(shift, self.plus_ex, self.string)

    def str_in_brackets(self, shift):
        return self.object_in_brackets(shift, self.string)


    #term

    def term(self, shift):

        str_item = self.string(shift)
        num_item = self.num(shift)
        bool_item = self.bool(shift)
        var_item = self.var_name(shift)

        max_moved_item = [None, False, 0]

        for item in [var_item, str_item, num_item, bool_item]:
            if item[1]:
                if max_moved_item[2] < item[2]:
                    max_moved_item = item

        tree = Tree()

        node_id = "Term" + self.get_uniq_postfix()
        tree.create_node("Term", node_id)

        if max_moved_item[0]:
            tree.paste(node_id, max_moved_item[0])

        return tree, max_moved_item != (None, False, 0), max_moved_item[2]


    #id_with_assignment_op

    def id_with_assignment_op(self, shift):
        tree = None
        var_name = self.var_name(shift)
        if var_name[1]:
            assignment_op = self.assignment_op_ex(shift + 1)
            augassign_ex = self.augassign_ex(shift + 1)
            if assignment_op[1] or augassign_ex[1]:
                tree = Tree()

                node_id = "id_with_assignment_op" + self.get_uniq_postfix()
                tree.create_node("Id with assignment", node_id)

                tree.paste(node_id, var_name[0])
                if assignment_op[1]:
                    tree.paste(node_id, assignment_op[0])
                else:
                    tree.paste(node_id, augassign_ex[0])

                #В отличие от других методов возвращает еще и node_id для удобного добавления в дерево
                return tree, True, shift + 2, node_id

        return tree, False, "Ждали присваивания"

    #expr

    def expr(self, shift, tab_count):

        for i in range(shift, shift + tab_count):
            if not self.tab_ex(i)[1]:
                return None, False

        id_with_assignment_op = self.id_with_assignment_op(shift + tab_count)
        term = self.term(shift + tab_count)

        if id_with_assignment_op[1]:
            inserted_term = self.term(id_with_assignment_op[2])
            if inserted_term[1]:

                tree = Tree()
                node_id = "Expr" + self.get_uniq_postfix()
                tree.create_node("Expression", node_id)
                tree.paste(node_id, id_with_assignment_op[0])
                tree.paste(node_id, inserted_term[0])
                return tree, True, inserted_term[2]

        if term[1]:
            tree = Tree()
            node_id = "Expr" + self.get_uniq_postfix()
            tree.create_node("Expression", node_id)
            tree.paste(node_id, term[0])
            return tree, True, term[2]

        return None, False, "Ждали выражения"

    # while

    def while_statement(self, shift, tab_count):
        return self.word_with_bool(shift, tab_count, self.while_ex, "While")

    # if_statement

    def if_statement(self, shift, tab_count):

        if_statement = self.word_with_bool(shift, tab_count, self.if_ex, "If")
        parse_res = False
        curr_shift = shift

        if if_statement[1]:
            parse_res = True
            curr_shift = if_statement[2]

            elif_statement = self.word_with_bool(curr_shift, tab_count, self.elif_ex, "Elif")

            while elif_statement[1]:
                curr_shift = elif_statement[2]
                if_statement[0].paste(if_statement[3], elif_statement[0])
                elif_statement = self.word_with_bool(curr_shift, tab_count, self.elif_ex, "Elif")

            else_statement = self.else_statement(curr_shift, tab_count)

            if else_statement[1]:
                if_statement[0].paste(if_statement[3], else_statement[0])
                curr_shift = else_statement[2]
        else:
            return None, False, "Ждали if'a"

        return if_statement[0], parse_res, curr_shift

    #else

    def else_statement(self, shift, tab_count):
        tree = Tree()
        node_id = "Else" + self.get_uniq_postfix()
        tree.create_node("Else", node_id)

        for i in range(shift, shift + tab_count):
            if not self.tab_ex(i)[1]:
                return tree, False

        if self.else_ex(shift)[1]:
            double_dot = self.double_dot_ex(shift+1)
            if double_dot[1]:
                statements = self.statements(shift + 2, tab_count + 1)
                if statements[1]:
                    tree.paste(node_id, statements[0])
                    return tree, True, statements[2], node_id
            else:
                return tree, False, "Ожидалось двоеточие"
        else:
            return tree, False, "Ожидался else-блок"

    # statement

    def statement(self, shift, tab_count):

        if shift > len(self.lexs) - 1:
            return None, False, "Ожидался оператор (if, while) или действие/присваивание"

        if_statement = self.if_statement(shift, tab_count)
        while_statement = self.while_statement(shift, tab_count)
        expr = self.expr(shift, tab_count)

        if if_statement[1]:
            return if_statement
        elif while_statement[1]:
            return while_statement
        elif expr[1]:
            return expr
        else:
            return None, False, "Ожидался оператор (if, while) или действие/присваивание"

    #statements

    def statements(self, shift, tab_count):

        tree = Tree()
        res = False
        curr_shift = shift

        pos = 0

        node_id = "Statements" + self.get_uniq_postfix()
        tree.create_node("Statements", node_id)

        statement = self.statement(shift, tab_count)

        while statement[1]:
            curr_stm_id = str(pos) + "_" + self.get_uniq_postfix()
            tree.create_node(identifier=curr_stm_id, parent=node_id)
            curr_shift = statement[2]
            res = True
            tree.paste(curr_stm_id, statement[0])
            statement = self.statement(statement[2], tab_count)
            pos += 1
        return tree, res, curr_shift


    #program
    def program(self):
        tree = Tree()
        res = False
        curr_shift = 0

        pos = 0

        node_id = "Statements" + self.get_uniq_postfix()
        tree.create_node("Statements", node_id)

        statement = self.statement(0, 0)

        while statement[1]:
            curr_stm_id = str(pos) + "_" + self.get_uniq_postfix()
            tree.create_node(identifier=curr_stm_id, parent=node_id)
            curr_shift = statement[2]
            res = True
            tree.paste(curr_stm_id, statement[0])
            statement = self.statement(statement[2], 0)
            pos += 1
            if not statement[1] and self.lattest_lex_num < len(self.lexs) - 1:
                print(statement[2])
                print(self.lattest_lex_num)

        return tree, res, curr_shift