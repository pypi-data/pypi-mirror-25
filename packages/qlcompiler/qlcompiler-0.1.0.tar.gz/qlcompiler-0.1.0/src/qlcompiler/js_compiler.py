from .compiler import Compiler


class JsCompiler(Compiler):
    """
    Javascript compiler.
    """


def compile(ql, **kwargs):
    """
    Compiles quick lambda object to Javascript.
    """

    compiler = JsCompiler(ql)
    return compiler.compile(**kwargs)