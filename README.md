## permute

A python package for compiling large branching python functions into iterative C code.

### Coding Guidelines

Use python `3.10+`

Use type hints in parameters and returns.

```python
def typed_function(a: int, b: int) -> int:
    return a + b
```

Use type hints in assignments to indicate initialization

```python
def foo():
    x: int = 0
    x = x + 1
```

When using type hints, do not use any of the now-deprecated *UpperCase* type classes from the `typing` package

```python
# do this ✔
x: list[float] = [0.1, 0.2, 0.3]
y: dict[str, int] = {
    'foo': 0,
    'bar': 1,
}

# not this ✖
from typing import List, Dict
x: List[int] = []
y: Dict[str, int] = {}
```

### Unsupported Language Features

- Classes & Objects, use `namedtuple` instead
- Iterable unpacking `a, b = (1, 2)`
- Keyword arguments `func(a=2)`
- Default arguments `def func(a: float = 2)`
- Variable length arguments `*args` and `**kwargs`

### WIP Language Features

- Dictionaries
