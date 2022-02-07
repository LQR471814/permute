import ast

import cgen as c

from typenames import primitives
from utils import parse_subscript, walk_tree


class MissingAnnotation(Exception):
    """Raised when a required type hint is not given in the code."""
    pass


class InconsistentAnnotation(Exception):
    """Raised when a type hint conflicts with another type hint of the same variable"""
    pass


class Options:
    def __init__(self, name: str):
        self._name = name

    def name(self, suffix: str) -> str:
        return self._name + suffix


def build_parameters(source: ast.FunctionDef, options: Options) -> c.Struct:
    fields = []
    for a in source.args.args:
        match a.annotation:
            case ast.Name():
                fields.append(primitives[a.annotation.id](a.arg))
            case None:
                raise MissingAnnotation
    return c.Struct(options.name("Parameters"), fields)


def build_returns(source: ast.FunctionDef, options: Options) -> c.Typedef:
    match source.returns:
        case ast.Name():
            return c.Typedef(primitives[source.returns.id](options.name("Returns")))
    raise MissingAnnotation


def build_stack(source: ast.FunctionDef, options: Options) -> c.Struct:
    fields = {}

    def visit_node(node: ast.AST, depth: int):
        match node:
            case ast.AnnAssign(target=var, annotation=ann):
                name = (
                    var.id if (var.id not in fields)
                    else f"{var.id}_{depth}"
                )
                if name in fields:
                    raise InconsistentAnnotation

                match ann:
                    case ast.Name(id=typename):
                        fields[name] = primitives[typename](name)
                    case ast.Subscript() as sub:
                        fields[name] = parse_subscript(sub, name)

    walk_tree(source, visit_node)
    return c.Struct(options.name("Stack"), fields.values())
