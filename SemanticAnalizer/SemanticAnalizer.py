from SemanticAnalizer.SemanticError import SemanticError


class SemanticAnalizer:

    types = ("Bool", "Num", "String")

    def __init__(self, tree):
        self.tree = tree

    def anilize(self, node=None, vars=None, type=None):

        node = self.tree.root if not node else node
        vars1 = {} if vars is None else vars

        for item in self.tree.children(node):
            if item.identifier.startswith("Expr"):
                vars1 = self.__check_expr__(item.identifier, vars1)
                continue
            elif item.tag.startswith(SemanticAnalizer.types):
                type = item.tag
            elif item.tag.startswith("var_name"):
                var_name = self.tree.children(item.identifier)[0].tag

                if var_name not in vars1.keys():
                    raise SemanticError("Неопределенная переменная " + var_name)
                elif type:
                    if vars1[var_name].upper()[0:3] != type.upper()[0:3]:
                        raise SemanticError("Трешовый тип у переменной " + var_name)

            self.anilize(item.identifier, vars1, type)

    def __check_expr__(self, node, vars):
        var_name = None
        type = None
        term = None

        for item in self.tree.children(node):
            if item.identifier.startswith("id_with_assignment_op"):
                var_name = self.__get_var_name__(item.identifier, vars)
                continue
            if item.identifier.startswith("Term"):
                term = item.identifier
                type = self.__get_var_type__(item.identifier, vars)
            self.anilize(item.identifier, vars)

        if type == "Id":
            ops = self.__get_operations__(term)
            used_vars = self.__get_used_vars__(term)

            used_var_type = vars[used_vars[0]]

            for var in used_vars:
                if used_var_type != vars[var]:
                    raise SemanticError("Несоответствие типов " + var)

            if vars[used_vars[0]] == "String":

                if var_name[1] != "+=":
                    raise SemanticError("Неприемлимое присваивание " + var_name[1])

                for op in ops:
                    if op != "+":
                        raise SemanticError("Неприемлимая операция " + op)

            vars[var_name[0]] = vars[used_vars[0]]

        elif var_name and type:
            vars[var_name[0]] = type
        return vars

    def __get_var_name__(self, node, vars):
        var_name = ""
        assignment = None

        for item in self.tree.children(node):
            if item.identifier.startswith("var_name"):
                var_name = self.tree.children(item.identifier)[0].tag
            else:
                assignment = item.tag

        if assignment != "=":
            if var_name not in vars.keys():
                raise SemanticError("Неопределенная переменная " + var_name)

        return var_name, assignment

    def __get_var_type__(self, node, vars):

        type = self.tree.children(node)[0]

        if type.identifier.startswith("var_name"):

            var_name = self.tree.children(type.identifier)[0]

            if vars is None:
                raise SemanticError("Неопределенная переменная " + var_name)
            elif var_name in vars.keys():
                    return vars[var_name]

        return type.tag

    def __get_operations__(self, node):

        ops = set()

        for item in self.tree.children(node):

            if item.tag.startswith(("+", "-", "/", "*", "or", "and")):
                ops.add(item.tag)
            else:
                ops = ops | self.__get_operations__(item.identifier)

        return ops

    def __get_used_vars__(self, node):

        used_vars = []

        for item in self.tree.children(node):
            if item.tag.startswith("var_name"):
                used_vars.append(self.tree.children(item.identifier)[0].tag)
            else:
                used_vars += self.__get_used_vars__(item.identifier)

        return used_vars
