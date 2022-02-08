import logging

from permute.transpiler import *


def recursive(func):
    return func


def build(source: str, name: str = "Permute"):
    tree = ast.parse(source)
    # print(ast.dump(tree, indent="  "))

    if isinstance(tree, ast.Module):
        for statement in tree.body:
            match statement:
                case ast.FunctionDef(
                    decorator_list=[
                        ast.Name(id='recursive'),
                        *_
                    ]
                ):
                    function = FunctionBuilder(statement, name)
                    logging.debug(
                        "="*30 +
                        f"\n{function.parameters}" +
                        f"\n{function.returns}" +
                        f"\n{function.stack}"
                    )
