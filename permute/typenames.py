import ast
import cgen as c
from typing import Generic, TypeVar

from permute.exceptions import UnimplementedError


T = TypeVar('T')


class Type(Generic[T]):
    typename: str = ""
    name: str
    defaultvalue: T

    def __init__(self, name: str, defaultvalue: T = None):
        self.name = name
        self.defaultvalue = defaultvalue

    def initialize(self) -> list[c.Generable]:
        raise Exception("Cannot initialize unknown type!")

    def get_type(self) -> c.Value:
        return c.Value(self.typename, self.name)


class Primitive(Type[ast.Constant]):
    def initialize(self) -> list[c.Generable]:
        value = ast.unparse(self.defaultvalue)
        if value == 'None':
            value = 'NULL'
        return [c.Assign(f'{self.typename} {self.name}', value)]


class Integer(Primitive):
    typename: str = "int"


class Float(Primitive):
    typename: str = "float"


class String(Type[ast.Constant]):
    typename: str = "String_T"


class List(Type[ast.List]):
    # note: the str in the type union refers to a variable name
    # not the string type
    typename: str = "List_T"

    def initialize(self) -> list[c.Generable]:
        rendered_elements: list[str] = []
        for e in self.defaultvalue.elts:
            match e:
                case ast.Constant(value=float() | int() as n):
                    rendered_elements.append(str(n))
                case ast.Constant(value=str()):
                    raise UnimplementedError(
                        message="Inline string within list!"
                    )
                case ast.Name(id=name):
                    rendered_elements.append(name)

        return [
            c.Pointer(c.Value(self.typename, self.name)),
            c.Statement(
                f"List_list({self.name}"
                f"{', ' if len(rendered_elements) > 0 else ''}"
                f"{', '.join(rendered_elements)})"
            )
        ]


class Dictionary(Type):
    typename: str = "Table_T"

    def __init__(self, name: str, defaultvalue: T):
        raise Exception("Dictionaries are currently unsupported!")


type_index: dict[str, Type] = {
    'int': Integer,
    'float': Float,
    'str': String,  # TODO: Implement string polyfill
    'list': List,
    'dict': Dictionary,
}
