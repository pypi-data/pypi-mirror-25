import pytest

from matchstick import match, NoMatchException

def test_does_not_break_function():
    @match('True')
    def f(a, b=2):
        return a + b
    assert f(3, 4) == 7
    assert f(2) == 4
    assert f(1, b=3) == 4

def test_simple_conditions():
    @match('x >= 0')
    def f(x):
        return x
    @match('x < 0')
    def f(x):
        return -x
    assert f(8) == 8
    assert f(3.5) == 3.5
    assert f(-2) == 2

def test_no_match():
    @match('False')
    def f(x):
        pass
    with pytest.raises(NoMatchException):
        f(3)

def test_different_types():
    @match('type(x) is int')
    def f(x):
        return x * 2
    @match('type(x) is float')
    def f(x):
        return x ** 2
    @match('type(x) is str and "{}" in x')
    def f(x):
        return x.format(12)
    assert f(13) == 26
    assert f(2.0) == 4.0
    assert f(2.5) == 6.25
    assert f('a{}c') == 'a12c'

def test_differing_arity():
    @match('True')
    def f(x):
        return x
    @match('True')
    def f(x, y):
        return x + y
    assert f(1) == 1
    assert f(2, 3) == 5
    with pytest.raises(NoMatchException):
        f()
    with pytest.raises(NoMatchException):
        f(4, 5, 6)

def test_more_complex():
    @match('type(x) is list and len(x) > 2 and x[2] == 4')
    def f(x):
        return x[:2]
    @match('True')
    def f(x):
        return x
    assert f([1, 2, 3, 4]) == [1, 2, 3, 4]
    assert f([0, 0, 4]) == [0, 0]
    assert f('a') == 'a'

def test_complex_signature():
    @match('x > 3 and y < x and z == x + y')
    def f(x, y=3, *, z):
        return x - y + z
    @match('type(x) is int and type(y) is str')
    def f(x, y='y'):
        return y + str(x)
    assert f(4, z=7) == 8
    assert f(123, 'abc') == 'abc123'
    assert f(0, y='x') == 'x0'
    assert f(12, y=7, z=19) == 24
    with pytest.raises(NoMatchException):
        f(4, y=4, z=3)
    with pytest.raises(NoMatchException):
        f(3.0, 'b')
