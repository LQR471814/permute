import ast


class MissingAnnotation(Exception):
    """Raised when a required type hint is not given in the code."""


class InconsistentAnnotation(Exception):
    """Raised when a type hint conflicts with another type hint of the same variable"""


# class InvalidAssignment(Exception):
#     """Raised when an invalid assignment that arises with dynamic typing occurs"""

#     def __init__(self, message: str):
#         super().__init__(f"Invalid assignment: {message}")

class UnimplementedError(Exception):
    """Raised when a specific language pattern hasn't been implemented yet"""

    def __init__(self, node: ast.AST = None, message: str = ""):
        msg = type(node).__name__ if ast.AST is not None else message
        super().__init__(f"Translation of {msg} is currently unimplemented")


class UnsupportedType(Exception):
    """Raised when an unsupported type is used"""

    def __init__(self, name: str):
        super().__init__(f"Unsupported type {name} used")
