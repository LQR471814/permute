import logging

from permute.transpiler import *
from permute.exceptions import *


def recursive(func):
    return func


def build(source: str, name: str = "Permute"):
    tree = ast.parse(source)

    if isinstance(tree, ast.Module):
        for statement in tree.body:
            match statement:
                case ast.FunctionDef(
                    decorator_list=[
                        ast.Name(id='recursive'),
                        *_
                    ]
                ):
                    print(ast.dump(statement, indent="  "))
                    function = FunctionBuilder(statement, name)
                    logging.debug(
                        "="*30 +
                        f"\n{function.parameters}" +
                        f"\n{function.returns}" +
                        f"\n{function.stack}" +
                        f"\n{function.body}"
                    )
