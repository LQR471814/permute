import ast
import typing

import cgen as c

from permute.translate import Translator
from permute.typenames import type_index
from permute.utils import unused_variable, walk_tree


class UnsupportedType(Exception):
    """Raised when an unsupported type is used"""


class MissingAnnotation(Exception):
    """Raised when a required type hint is not given in the code."""


class InconsistentAnnotation(Exception):
    """Raised when a type hint conflicts with another type hint of the same variable"""


class Var:
    def __init__(self, name: str, typename: str):
        self.name = name
        self.typename = typename

    def toC(self):
        return c.Value(type_index[self.typename], self.name)


class FunctionBuilder:
    __variables: typing.Dict[str, Var] = {}

    def __init__(self, source: ast.FunctionDef, name: str) -> None:
        self.name = name
        self.source = source

        self.returns = self.__build_returns()
        self.parameters = self.__build_parameters()
        self.stack = self.__build_stack()

    def __name(self, suffix: str) -> str:
        return self.name + suffix

    def __assign_var(self, name: str, typename: str) -> c.Value:
        self.__variables[name] = Var(name, typename)
        return self.__variables[name].toC()

    def __build_parameters(self) -> c.Struct:
        fields = []
        for a in self.source.args.args:
            match a.annotation:
                case ast.Name():
                    fields.append(self.__assign_var(a.arg, a.annotation.id))
                case None:
                    raise MissingAnnotation
        return c.Struct(self.__name("Parameters"), fields)

    def __build_returns(self) -> c.Typedef:
        match self.source.returns:
            case ast.Name():
                return c.Typedef(
                    c.Value(
                        name=self.__name("Returns"),
                        typename=self.source.returns.id
                    )
                )
        raise MissingAnnotation

    def __build_stack(self) -> c.Struct:
        fields = {}

        def make_name(name: str, depth: int) -> str:
            name = (
                name if (name not in fields)
                else f"{name}_{depth}"
            )
            if name in fields:
                raise InconsistentAnnotation
            return name

        def visit_node(node: ast.AST, depth: int):
            match node:
                case ast.AnnAssign(target=var, annotation=ann):
                    name = make_name(var.id, depth)
                    match ann:
                        case ast.Name(id=typename):
                            fields[name] = self.__assign_var(name, typename)
                        case ast.Subscript() as sub:
                            fields[name] = self.__assign_var(
                                name, sub.value.id
                            )
                case ast.For(
                    target=var,
                    iter=ast.Call(func=ast.Name(id='range'))
                ):
                    if not unused_variable(var.id):
                        name = make_name(var.id, depth)
                        fields[name] = self.__assign_var(name, 'int')

        walk_tree(self.source, visit_node)
        return c.Struct(self.__name("Stack"), fields.values())

    def __build_body(self) -> c.FunctionBody:
        pass


class PermutativeTranslator(Translator):
    pass
