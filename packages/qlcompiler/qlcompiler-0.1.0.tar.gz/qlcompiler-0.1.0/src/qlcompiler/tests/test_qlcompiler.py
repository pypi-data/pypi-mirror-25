import pytest
import qlcompiler


def test_project_defines_author_and_version():
    assert hasattr(qlcompiler, '__author__')
    assert hasattr(qlcompiler, '__version__')
