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


def unused_variable(name: str) -> bool:
    return re.match(r'_+', name)


def contains_node(root: ast.AST, target: ast.AST) -> bool:
    for node in ast.iter_child_nodes(root):
        if isinstance(node, target) or contains_node(node, target):
            return True
    return False

# def is_iterable(typename: str) -> bool:
#     iterable = True
#     try:
#         iter(eval(typename))
#     except:
#         iterable = False
#     return iterable
