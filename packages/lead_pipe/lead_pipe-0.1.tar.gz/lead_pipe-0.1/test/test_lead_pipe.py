import pytest

from lead_pipe import apply, Pipe, reflect

def test_apply():
    assert ~Pipe('{a} {}'.format)(apply, 2, a=1) == '1 2'

def test_create():
    assert ~Pipe(10) == 10

def test_reflect():
    assert ~Pipe({'a': 1})(reflect, 'get', 'a') == 1

def test_simple():
    assert ~Pipe(12)(str) == '12'
