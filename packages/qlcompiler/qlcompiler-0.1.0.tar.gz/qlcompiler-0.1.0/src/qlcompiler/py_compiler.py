from .compiler import Compiler


class PyCompiler(Compiler):
    """
    Python compiler.
    """


def compile(ql, **kwargs):
    """
    Compiles quick lambda object to Python.
    """

    compiler = PyCompiler(ql)
    return compiler.compile(**kwargs)
