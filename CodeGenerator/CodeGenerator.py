import collections


class CodeGenerator:
    __tree = None
    __js_code = None

    def __init__(self, tree):
        self.__tree = tree

    def get_js_code(self):
        self.__js_code = self.stataments(self.__tree.root)

    def write_code_to_file(self, file_name):

        if not self.__js_code:
            self.get_js_code()

        with open(file_name, "w") as text_file:
            text_file.write(self.__js_code)

    def elem_op(self, node, main_name):

        op = None
        elem = None

        for item in self.__tree.children(node):
            if item.tag != main_name:
                op = item.tag
            else:
                elem = item

        js_ops_conformity = {"or": "||", "and": "&&"}

        if op in js_ops_conformity.keys():
            op = js_ops_conformity[op]

        return op, elem

    def term_content(self, node, main_name, var_type, op_title, brackets_title):
        simple_elem = ""
        elem_op = None
        not_op = None
        bool = None

        for item in self.__tree.children(node.identifier):
            if item.tag == var_type or item.tag == "var_name":
                if item.tag == "bools":
                    simple_elem = self.__tree.children(item.identifier)[0].tag.lower()
                else:
                    simple_elem = self.__tree.children(item.identifier)[0].tag
            elif item.tag == brackets_title:
                return "(" + self.term_content(self.__tree.children(item.identifier)[0], main_name, var_type, op_title,
                                               brackets_title) + ")"
            elif item.tag == op_title:
                elem_op = self.elem_op(item.identifier, main_name)
            elif item.tag == "Compare nums":
                return self.compare_nums(item)
            elif item.tag == "not":
                not_op = "!"
            elif item.tag == "Bool":
                bool = self.bool(item)

        if elem_op:
            return simple_elem + " " + elem_op[0] + " " + self.term_content(elem_op[1], main_name, var_type, op_title,
                                                                brackets_title)
        elif not_op:
            return not_op + " " + bool

        return simple_elem

    def num(self, node):
        return self.term_content(node, "Num", "num", "Operation with number", "Number in brackets")

    def bool(self, node):
        return self.term_content(node, "Bool", "bools", "Operation with bool", "Bool in brackets")

    def string(self, node):
        return self.term_content(node, "String", "string", "Operation with string", "String in brackets")

    def id(self, node):
        return self.term_content(node, "Id", "", "Operation with id", "Id in brackets")

    def term(self, node):

        term_content = self.__tree.children(node.identifier)[0]

        if term_content.tag == "Num":
            return self.num(term_content)
        elif term_content.tag == "String":
            return self.string(term_content)
        elif term_content.tag == "Bool":
            return self.bool(term_content)
        elif term_content.tag == "Id":
            return self.id(term_content)

        print("что-то пошло не так")
        exit(500)

    def expression(self, node):
        id_with_assignment = None
        term = None

        for item in self.__tree.children(node.identifier):
            if item.tag == "Id with assignment":
                id_with_assignment = self.id_with_assignment(item)
            else:
                term = self.term(item)

        return id_with_assignment + " " + term

    def id_with_assignment(self, node):

        var_name = None
        assignment = None

        for item in self.__tree.children(node.identifier):
            if item.tag == "var_name":
                var_name = self.__tree.children(item.identifier)[0].tag
            else:
                assignment = item.tag

        return var_name + " " + assignment

    def while_block(self, node):
        bool = None
        statements = None

        for item in self.__tree.children(node.identifier):
            if item.tag == "Bool":
                bool = self.bool(item)
            else:
                statements = self.stataments(item)

        return "while(" + bool + ") {\n" + statements + "}\n"

    def if_block(self, node):

        bool = None
        statements = None
        elifs = {}
        else_statements = None

        for item in self.__tree.children(node.identifier):

            if item.tag == "Bool":
                bool = self.bool(item)
            elif item.tag == "Statements":
                statements = self.stataments(item)
            elif item.tag == "Else":
                else_statements = self.stataments(self.__tree.children(item.identifier)[0])
            else:
                elifs[int(item.tag)] = self.elif_block(self.__tree.children(item.identifier)[0])

        elifs_text = ""

        for num, value in collections.OrderedDict(sorted(elifs.items())).items():
            elifs_text += value

        all_if_code = "\nif(" + bool + ") {\n" + statements + "}\n" + elifs_text

        if else_statements:
            all_if_code += "else{\n" + else_statements + "}\n"

        return all_if_code

    def elif_block(self, node):
        bool = None
        statements = None

        for item in self.__tree.children(node.identifier):
            if item.tag == "Bool":
                bool = self.bool(item)
            else:
                statements = self.stataments(item)

        return "else if(" + bool + ") {\n" + statements + "}\n"

    def stataments(self, node):

        if not type(node) == str:
            node = node.identifier

        statements = {}

        for item in self.__tree.children(node):
            statements[int(item.tag)] = self.statament(self.__tree.children(item.identifier)[0])

        statements_text = ""
        for num, value in collections.OrderedDict(sorted(statements.items())).items():
            statements_text += value

        return statements_text

    def statament(self, node):

        if node.tag == "If":
            return self.if_block(node)
        elif node.tag == "While":
            return self.while_block(node)
        elif node.tag == "Expression":
            return self.expression(node) + ";\n"

        print("что-то пошло не так")
        exit(500)

    def compare_nums(self, node):

        op = None
        nums = {}

        for item in self.__tree.children(node.identifier):
            if item.tag == "op":
                op = self.__tree.children(item.identifier)[0].tag
            else:
                nums[item.tag] = self.num(self.__tree.children(item.identifier)[0])

        compare_code = ""

        nums = list(collections.OrderedDict(sorted(nums.items())).items())

        return nums[0][1] + " " + op + " " + nums[1][1]
