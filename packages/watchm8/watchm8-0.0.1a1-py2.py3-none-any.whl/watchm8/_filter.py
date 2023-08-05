# -*- coding: utf-8 -*-

from __future__ import print_function
import ast
import _ast


class Filter(object):

    def __init__(self, expr):
        self._plain_expr = expr
        self._expr = ast.parse(expr, mode='eval')

    @property
    def expr(self):
        return self._plain_expr

    def __call__(self, event, emitter):
        return RootVisitor(
            {'event': event, 'emitter': emitter}
        ).visit(self._expr)


def _getattr(obj, attr):
    # Resolve globals / reserved keywords
    if attr == 'None':
        return None
    elif attr == 'True':
        return True
    elif attr == 'False':
        return False

    if type(obj) is dict:
        '''
        Potential conflicts in dict key vs obj attr resolution:
        '__class__', '__cmp__', '__contains__', '__delattr__', '__delitem__',
        '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__',
        '__getitem__', '__gt__', '__hash__', '__init__', '__iter__', '__le__',
        '__len__', '__lt__', '__ne__', '__new__', '__reduce__',
        '__reduce_ex__', '__repr__', '__setattr__', '__setitem__',
        '__sizeof__', '__str__', '__subclasshook__', 'clear', 'copy',
        'fromkeys', 'get', 'has_key', 'items', 'iteritems', 'iterkeys',
        'itervalues', 'keys', 'pop', 'popitem', 'setdefault', 'update',
        'values', 'viewitems', 'viewkeys', 'viewvalues'
        '''

        # MRO: dict key, obj attr
        try:
            return obj[attr]
        except KeyError:
            pass

        try:
            return getattr(obj, attr)
        except:
            return None
    else:
        return getattr(obj, attr)


class ExpressionVisitor(ast.NodeVisitor):

    def __init__(self, doc):
        ast.NodeVisitor.__init__(self)
        self._doc = doc

    def visit_Compare(self, node):
        _left = self.visit(node.left)
        _op = node.ops[0]
        _comparator = self.visit(node.comparators[0])  # Fix: multi ops 1,2,3

        if type(_op) is ast.Eq:
            return _left == _comparator
        elif type(_op) is ast.NotEq:
            return _left != _comparator
        elif type(_op) is ast.Lt:
            return _left < _comparator
        elif type(_op) is ast.LtE:
            return _left <= _comparator
        elif type(_op) is ast.Gt:
            return _left > _comparator
        elif type(_op) is ast.GtE:
            return _left >= _comparator
        elif type(_op) is ast.Is:
            return _left is _comparator
        elif type(_op) is ast.IsNot:
            return _left is not _comparator

    def visit_Attribute(self, node):
        try:
            return _getattr(self.visit(node.value), node.attr)
        except:
            return None

    def visit_Name(self, node):
        try:
            return _getattr(self._doc, node.id)
        except:
            return None

    def visit_NameConstant(self, node):
        return node.value

    def visit_Call(self, node):
        _func = self.visit(node.func)

        if _func is None:
            return None

        args = []
        for a in node.args:
            args.append(self.visit(a))

        kwargs = {}
        for kw in node.keywords:
            kwargs.update({kw.arg: self.visit(kw.value)})

        return _func(*args, **kwargs)

    def visit_Subscript(self, node):
        value = self.visit(node.value)

        if type(node.slice) is _ast.Slice:
            _lower = self.visit(node.slice.lower)
            _upper = self.visit(node.slice.upper)
            _step = None

            if node.slice.step is not None:
                _step = self.visit(node.slice.step)

            return value[_lower:_upper:_step]

        idx = self.visit(node.slice)
        return value[idx]

    def visit_Index(self, node):
        if type(node.value) is _ast.Str:
            raise SyntaxError('Invalid syntax')

        return self.visit(node.value)

    def visit_BoolOp(self, node):
        if type(node.op) is _ast.And:
            return all([self.visit(v) for v in node.values])
        elif type(node.op) is _ast.Or:
            return any([self.visit(v) for v in node.values])

    def visit_Num(self, node):
        return node.n

    def visit_Str(self, node):
        return node.s

    def generic_visit(self, node):
        raise SyntaxError('Illegal statement.')


class RootVisitor(ast.NodeVisitor):

    def __init__(self, doc):
        ast.NodeVisitor.__init__(self)
        self._doc = doc

    def visit_Expression(self, node):
        v = ExpressionVisitor(self._doc)
        return v.visit(node.body)

    def generic_visit(self, node):
        raise SyntaxError('Illegal expression.')
