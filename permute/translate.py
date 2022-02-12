import ast
import cgen as c
from permute.exceptions import UnimplementedError
from permute.typenames import type_index


class Translator:
    def translate_initialization(self, node: ast.AnnAssign) -> list[c.Generable]:
        match node.annotation:
            case ast.Name(id=name) | ast.Subscript(value=ast.Name(id=name)):
                return type_index[name](node.target.id, node.value).initialize()
        raise UnimplementedError(node)

    def translate_assignment(self, node: ast.Assign) -> c.Assign:
        if len(node.targets) > 1:
            raise UnimplementedError(message='iterable unpacking')

        match node.targets[0]:
            case ast.Name():
                return c.Assign(node.targets[0].id, ast.unparse(node.value))

        raise UnimplementedError(node.targets[0])

    def translate_call(self, node: ast.Call) -> c.Statement:
        if len(node.keywords) > 0:
            raise UnimplementedError(message="keyword arguments")
        return c.Statement(ast.unparse(node))

    def translate_if(self, node: ast.If, body: c.Block) -> c.If:
        return c.If(ast.unparse(node.test), body)

    def translate_for(self, node: ast.For, body: c.Block) -> c.For:
        match node:
            case ast.For(
                target=ast.Name(id=name),
                iter=ast.Call(
                    func=ast.Name(id='range'),
                    args=[ast.Constant(value=end)]
                )
            ):
                return c.For(f"int {name} = 0", f"i < {end}", "i++", body)
            case ast.For(
                target=ast.Name(id=name),
                iter=ast.Call(
                    func=ast.Name(id='range'), args=[
                        ast.Constant(value=start),
                        ast.Constant(value=end)
                    ]
                )
            ):
                return c.For(f"int {name} = {start}", f"i < {end}", "i++", body)
            case ast.For(
                target=ast.Name(id=name),
                iter=ast.Call(
                    func=ast.Name(id='range'),
                    args=[
                        ast.Constant(value=start),
                        ast.Constant(value=end),
                        ast.Constant(value=step)
                    ]
                )
            ):
                return c.For(f"int {name} = {start}", f"i < {end}", f"i += {step}", body)

        raise UnimplementedError(node)

    def translate_while(self, node: ast.While, body: c.Block) -> c.While:
        return c.While(
            ast.unparse(node.test),
            body,
        )

    def translate_return(self, node: ast.Return) -> c.Statement:
        return c.Statement(ast.unparse(node))

    def translate_break(self) -> c.Statement:
        return c.Statement('break')

    def translate_continue(self) -> c.Statement:
        return c.Statement('continue')


#? I am aware this shares the same instance of Translator() in the default value
def translate(source: list[ast.AST], t: Translator = Translator()) -> c.Block:
    body = []

    for n in source:
        match n:
            case ast.AnnAssign():
                for statement in t.translate_initialization(n):
                    body.append(statement)
            case ast.Assign():
                body.append(t.translate_assignment(n))
            case ast.Call():
                body.append(t.translate_call(n))
            case ast.If():
                body.append(t.translate_if(n, translate(n.body, t)))
            case ast.For():
                body.append(t.translate_for(n, translate(n.body, t)))
            case ast.While():
                body.append(t.translate_while(n, translate(n.body, t)))
            case ast.Return():
                body.append(t.translate_return(n))
            case ast.Break():
                body.append(t.translate_break())
            case ast.Continue():
                body.append(t.translate_continue())
            case ast.Expr():
                for statement in translate([n.value]).contents:
                    body.append(statement)
            case ast.Pass():
                pass
            case _:
                raise UnimplementedError(n)

    return c.Block(body)
