import ast
import re
from typing import Callable


def walk_tree(
    root: ast.AST,
    callback: Callable[[ast.AST, int], None],
    depth: int = 0
):
    for node in ast.iter_child_nodes(root):
        callback(node, depth)
        walk_tree(node, callback, depth+1)


def parse_subscript(sub: ast.Subscript) -> str:
    slicetype = sub.value
    if isinstance(sub.slice, ast.Subscript):
        slicetype = parse_subscript(sub.slice)
    return slicetype


def unused_variable(name: str) -> bool:
    return re.match(r'_+', name)
