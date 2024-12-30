import io
import ast

class _ImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.imported_modules = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imported_modules.append(alias.name)

    def visit_ImportFrom(self, node):
        module = node.module
        for alias in node.names:
            self.imported_modules.append(module)


def get_deps_list(source_path):
    with io.open(source_path) as f:
        source_code = f.read()

    tree = ast.parse(source_code)
    visitor = _ImportVisitor()
    visitor.visit(tree)

    return visitor.imported_modules
