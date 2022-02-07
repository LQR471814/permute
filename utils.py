import ast
from typing import Callable

import cgen as c

from typenames import collections


def walk_tree(
    root: ast.AST,
    callback: Callable[[ast.AST, int], None],
    depth: int = 0
):
    for node in ast.iter_child_nodes(root):
        callback(node, depth)
        walk_tree(node, callback, depth+1)


def parse_subscript(sub: ast.Subscript, name: str) -> c.Value:
    slicetype = sub.value
    if isinstance(sub.slice, ast.Subscript):
        slicetype = parse_subscript(sub.slice)
    return collections[slicetype.id](name)
