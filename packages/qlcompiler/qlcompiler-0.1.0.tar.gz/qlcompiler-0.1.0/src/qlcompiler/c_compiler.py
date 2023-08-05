from .compiler import Compiler


class CCompiler(Compiler):
    """
    C compiler.
    """


def compile(ql, **kwargs):
    """
    Compiles quick lambda object to C.
    """

    compiler = CCompiler(ql)
    return compiler.compile(**kwargs)