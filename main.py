import ast
import logging

from transpiler import Options, build_parameters, build_returns, build_stack


def transform(source: ast.FunctionDef, options: Options):
    # print(ast.dump(source, indent="  "))

    parameters = build_parameters(source, options)
    returns = build_returns(source, options)
    stack = build_stack(source, options)

    logging.debug(
        "="*30+
        f"\n{parameters}"+
        f"\n{returns}"+
        f"\n{stack}"
    )


def parse(source: str, options: Options = None):
    if options is None:
        options = Options("Permute")

    tree = ast.parse(source)
    if isinstance(tree, ast.Module):
        for statement in tree.body:
            if isinstance(statement, ast.FunctionDef):
                transform(statement, options)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    with open('example.py', mode="r") as f:
        parse(f.read())
