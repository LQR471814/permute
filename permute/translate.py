import ast
import cgen as c


class UnimplementedError(Exception):
    """Raised when a specific language pattern hasn't been implemented yet"""


class Translator:
    def translate(self, nodes: list[ast.AST]) -> c.Block:
        body = []

        for n in nodes:
            match n:
                case ast.If():
                    body.append(
                        self.translate_if(
                            n, self.translate(n.body)
                        )
                    )
                case ast.For():
                    body.append(
                        self.translate_for(
                            n, self.translate(n.body)
                        )
                    )

        return c.Block(body)

    def translate_if(self, node: ast.If, body: c.Block) -> c.If:
        return c.If(ast.unparse(node.test), body)

    def translate_for(self, node: ast.For, body: c.Block) -> c.For:
        match node:
            case ast.For(
                iter=ast.Call(
                    func=ast.Name(id='range', args=[ast.Constant(value=end)])
                )
            ):
                return c.For("int i = 0", f"i < {end}", "i++", body)
            case ast.For(
                iter=ast.Call(
                    func=ast.Name(id='range', args=[ast.Constant(
                        value=start), ast.Constant(value=end)])
                )
            ):
                return c.For(f"int i = {start}", f"i < {end}", "i++", body)
            case ast.For(
                iter=ast.Call(
                    func=ast.Name(id='range', args=[ast.Constant(
                        value=start), ast.Constant(value=end), ast.Constant(value=step)])
                )
            ):
                return c.For(f"int i = {start}", f"i < {end}", f"i += {step}", body)
        raise UnimplementedError

    def translate_while(self, node: ast.While, body: c.Block) -> c.While:
        pass
