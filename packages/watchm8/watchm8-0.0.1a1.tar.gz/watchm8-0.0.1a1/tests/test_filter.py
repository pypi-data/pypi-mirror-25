import pytest
from ast import parse, dump
from watchm8._filter import RootVisitor


def pprint(p):
    print(dump(p))


def test_simple_expression():
    RootVisitor({}).visit(parse('a == 1', mode='eval'))

    v = RootVisitor({'a': True}).visit(parse('a is True', mode='eval'))
    assert v is True

    v = RootVisitor({'a': False}).visit(parse('a is not True', mode='eval'))
    assert v is True


def test_nested_key():
    v = RootVisitor({'a': {'b': {'c': 1}}})\
        .visit(parse('a.b.c == 1', mode='eval'))
    assert v is True


def test_func_call():
    v = RootVisitor({'a': "BLA"})\
        .visit(parse('a.lower() == "bla"', mode='eval'))
    assert v is True

    v = RootVisitor({'a': {'bla': 1}})\
        .visit(parse('a.get("bla", None)', mode='eval'))
    assert v == 1

    v = RootVisitor({})\
        .visit(parse('"BLA".lower() == "bla"', mode='eval'))
    assert v is True


def test_non_existing_key():
    v = RootVisitor({})\
        .visit(parse('a.lower() == "bla"', mode='eval'))
    assert v is False


def test_slicing():
    v = RootVisitor({'a': [1, 2, 3]})\
        .visit(parse('a[0] == 1', mode='eval'))
    assert v is True

    v = RootVisitor({'a': [1, 2, 3]})\
        .visit(parse('a[0:2].count(1) == 1', mode='eval'))
    assert v is True

    with pytest.raises(SyntaxError):
        RootVisitor({'a': {'bla': 1}})\
            .visit(parse('a["bla"] == 1', mode='eval'))


def test_conjunction():
    v = RootVisitor({'a': 1, 'b': 1})\
        .visit(parse('a == 1 and b == 1', mode='eval'))
    assert v is True

    v = RootVisitor({'a': 1, 'b': 2})\
        .visit(parse('a == 1 and b == 1', mode='eval'))
    assert v is False


def test_disjunction():
    v = RootVisitor({'a': 1, 'b': 2})\
        .visit(parse('a == 1 or b == 1', mode='eval'))
    assert v is True

    v = RootVisitor({'a': 2, 'b': 2})\
        .visit(parse('a == 1 or b == 1', mode='eval'))
    assert v is False


def test_length():
    '''length() method not supported by Python needs to be injected'''


def test_funcs():
    with pytest.raises(SyntaxError):
        RootVisitor({})\
            .visit(parse('len([1, 2, 3])'))


def test_expression_only():
    with pytest.raises(SyntaxError):
        RootVisitor({}).visit(parse('import foo', mode='exec'))
