from sidekick import _
from qlcompiler import py_compiler


class TestPyCompiler:
    def test_simple_examples(self):
        comp = py_compiler.compile
        
        assert comp(_ + 1) == 'lambda _: _ + 1'
        assert comp(1 + _) == 'lambda _: 1 + _'
        assert comp(_[0] + 1) == 'lambda _: _[0] + 1'
        assert comp(_.foo(42) + 1) == 'lambda _: _.foo(42) + 1'
