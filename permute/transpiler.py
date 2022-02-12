import ast

import cgen as c
from permute.exceptions import InconsistentAnnotation, MissingAnnotation

from permute.translate import Translator, translate
from permute.typenames import Type, type_index
from permute.utils import unused_variable, walk_tree


class FunctionBuilder:
    __variables: dict[str, Type] = {}

    def __init__(self, source: ast.FunctionDef, name: str) -> None:
        self.name = name
        self.source = source

        self.declarator = self.__build_declarator()
        self.returns = c.Typedef(c.Value(
            name=self.__name("Returns"),
            typename=self.__get_returns()
        ))

        self.parameters = c.Struct(
            self.__name("Parameters"),
            self.declarator.arg_decls
        )

        self.stack = self.__build_stack()
        self.body = self.__build_body()

    def __name(self, suffix: str) -> str:
        return self.name + suffix

    def __assign_var(self, name: str, typename: str) -> c.Value:
        self.__variables[name] = type_index[typename](name, None)
        return self.__variables[name].get_type()

    def __build_declarator(self) -> c.FunctionDeclaration:
        return c.FunctionDeclaration(
            c.Value(self.__get_returns(), self.__name('')),
            self.__get_parameters()
        )

    def __get_parameters(self) -> list[c.Value]:
        fields = []
        for a in self.source.args.args:
            match a.annotation:
                case ast.Name():
                    fields.append(self.__assign_var(
                        a.arg,
                        a.annotation.id
                    ))
                case None:
                    raise MissingAnnotation
        return fields

    def __get_returns(self) -> str:
        match self.source.returns:
            case ast.Name():
                return type_index[self.source.returns.id].typename
            case ast.Subscript():
                return type_index[self.source.returns.value.id].typename
            case None:
                return 'void'
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
                            fields[name] = self.__assign_var(
                                name, typename
                            )
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
        return c.FunctionBody(
            fdecl=self.declarator,
            body=translate(self.source.body, Translator())
        )


class PermutativeTranslator(Translator):
    pass
