
class SemanticAnalizer:

    types = ("Bool", "Num", "String")

    def __init__(self, tree):
        self.tree = tree

    def start_anilize(self, node=None, vars=None, type=None):

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
                    print("Опять трешовая переменная " + var_name)
                    exit()
                elif vars1[var_name].upper()[0:3] != type.upper()[0:3]:
                    print("Трешовый тип у переменной " + var_name)
                    exit()

            self.start_anilize(item.identifier, vars1, type)

    def __check_expr__(self, node, vars):
        var_name = None
        type = None

        for item in self.tree.children(node):
            if item.identifier.startswith("id_with_assignment_op"):
                var_name = self.__get_var__(item.identifier, vars)
                continue
            if item.identifier.startswith("Term"):
                type = self.__get_var_type__(item.identifier, vars)
            self.start_anilize(item.identifier, vars)
        if var_name and type:
            vars[var_name] = type
        print(vars)
        return vars

    def __get_var__(self, node, vars):
        is_simple_assignment = True
        var_name = ""

        for item in self.tree.children(node):
            if item.identifier.startswith("var_name"):
                var_name = self.tree.children(item.identifier)[0].tag
            elif item.tag != "=":
                is_simple_assignment = False

        if not is_simple_assignment:
            if var_name not in vars.keys():
                print("Неопределенная переменная " + var_name)
                exit()
        else:
            return var_name

    def __get_var_type__(self, node, vars):
        type = self.tree.children(node)[0]
        if type.identifier.startswith("var_name"):
            var_name = self.tree.children(type.identifier)[0]
            if vars is None:
                print("Неопределенная переменная " + var_name)
                exit()
            elif var_name in vars.keys():
                    return vars[var_name]
        else:
            return type.tag