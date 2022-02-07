import cgen as c

primitives = {
    'int': lambda n: c.Value("int", n),
    'float': lambda n: c.Value("float", n),
    'str': lambda n: c.Pointer(c.Value("char", n)),
    'UNKNOWN': lambda n: c.Value("unknown", n),
}

collections = {
    'list': lambda n: c.Value(f"List_T", n),
    'dict': lambda n: c.Value(f"Table_T", n),
}
