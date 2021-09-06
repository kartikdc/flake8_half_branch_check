import ast
import sys
from typing import Any

# from typing import Dict
from typing import Generator
from typing import List
from typing import Tuple
from typing import Type


if sys.version_info < (3, 8):  # pragma: no cover (<PY38)
    import importlib_metadata
else:  # pragma: no cover (PY38+)
    import importlib.metadata as importlib_metadata


HBC101 = "HBC101 `if` block should end with an `else` statement"  # noqa: E501


class Visitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.errors: List[Tuple[int, int, str]] = []

    def visit_Module(self, node: ast.Module):
        for child in node.body:
            if not isinstance(child, ast.If):
                self.visit(child)

    def visit_If(self, node: ast.If):
        if not node.orelse:
            self.errors.append(
                (
                    node.lineno,
                    node.col_offset,
                    HBC101,
                )
            )
        self.generic_visit(node)


class Plugin:
    name = __name__
    version = importlib_metadata.version(__name__)

    def __init__(self, tree: ast.AST):
        self._tree = tree

    def run(self) -> Generator[Tuple[int, int, str, Type[Any]], None, None]:
        visitor = Visitor()
        visitor.visit(self._tree)

        for line, col, msg in visitor.errors:
            yield line, col, msg, type(self)
