'''An example extension for flake8 that checks for disrespectful code'''
import ast

__version__ = '0.0.1'

class DisrespectfulFunction(ast.NodeVisitor):
    violations = []

    def visit_FunctionDef(self, node):
        if len(node.name) == 1:
            self.violations.append(node)

        self.generic_visit(node)


class DisrespectfulCode:
    name = __name__
    version = __version__

    def __init__(self, tree, filename):
        self.tree = tree

    def run(self):
        func_visitor = DisrespectfulFunction()
        func_visitor.visit(self.tree)
        msg = 'X9000 stop creating function names with a single character. I expected more from you.'

        for node in func_visitor.violations:
            yield node.lineno, node.col_offset, msg, type(self)
