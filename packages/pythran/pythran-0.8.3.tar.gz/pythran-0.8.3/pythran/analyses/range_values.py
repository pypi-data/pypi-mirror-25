""" Module Analysing code to extract positive subscripts from code.  """
# TODO check bound of while and if for more occurate values.

import gast as ast
import copy

from pythran.analyses import Globals, Aliases
from pythran.intrinsic import Intrinsic
from pythran.passmanager import FunctionAnalysis
from pythran.interval import Interval, UNKNOWN_RANGE


def combine(op, node0, node1):
    key = '__{}__'.format(op.__class__.__name__.lower())
    try:
        return getattr(Interval, key)(node0, node1)
    except AttributeError:
        return UNKNOWN_RANGE


class RangeValues(FunctionAnalysis):

    """
    This analyse extract positive subscripts from code.

    It is flow insensitive and aliasing is not taken into account as integer
    doesn't create aliasing in Python.

    >>> import gast as ast
    >>> from pythran import passmanager, backend
    >>> node = ast.parse('''
    ... def foo(a):
    ...     for i in __builtin__.range(1, 10):
    ...         c = i // 2''')
    >>> pm = passmanager.PassManager("test")
    >>> res = pm.gather(RangeValues, node)
    >>> res['c'], res['i']
    (Interval(low=0, high=5), Interval(low=1, high=10))
    """

    def __init__(self):
        """Initialize instance variable and gather globals name information."""
        self.result = dict()
        super(RangeValues, self).__init__(Globals, Aliases)

    def add(self, variable, range_):
        """
        Add a new low and high bound for a variable.

        As it is flow insensitive, it compares it with old values and update it
        if needed.
        """
        if variable not in self.result:
            self.result[variable] = range_
        else:
            self.result[variable].union_update(range_)

    def visit_FunctionDef(self, node):
        """ Set default range value for globals and attributes.

        >>> import gast as ast
        >>> from pythran import passmanager, backend
        >>> node = ast.parse("def foo(a, b): pass")
        >>> pm = passmanager.PassManager("test")
        >>> res = pm.gather(RangeValues, node)
        >>> res['a']
        Interval(low=-inf, high=inf)
        """
        for global_name in self.globals:
            self.result[global_name] = UNKNOWN_RANGE
        for attr in node.args.args:
            self.result[attr.id] = UNKNOWN_RANGE

        for stmt in node.body:
            self.visit(stmt)

    def visit_Assign(self, node):
        """
        Set range value for assigned variable.

        We do not handle container values.

        >>> import gast as ast
        >>> from pythran import passmanager, backend
        >>> node = ast.parse("def foo(): a = b = 2")
        >>> pm = passmanager.PassManager("test")
        >>> res = pm.gather(RangeValues, node)
        >>> res['a']
        Interval(low=2, high=2)
        >>> res['b']
        Interval(low=2, high=2)
        """
        assigned_range = self.visit(node.value)
        for target in node.targets:
            if isinstance(target, ast.Name):
                # Make sure all Interval doesn't alias for multiple variables.
                self.add(target.id, copy.deepcopy(assigned_range))

    def visit_AugAssign(self, node):
        """ Update range value for augassigned variables.

        >>> import gast as ast
        >>> from pythran import passmanager, backend
        >>> node = ast.parse("def foo(): a = 2; a -= 1")
        >>> pm = passmanager.PassManager("test")
        >>> res = pm.gather(RangeValues, node)
        >>> res['a']
        Interval(low=1, high=2)
        """
        if isinstance(node.target, ast.Name):
            res = combine(node.op,
                          self.result[node.target.id],
                          self.visit(node.value))
            self.result[node.target.id].union_update(res)

    def visit_For(self, node):
        """ Handle iterate variable in for loops.

        >>> import gast as ast
        >>> from pythran import passmanager, backend
        >>> node = ast.parse('''
        ... def foo():
        ...     a = b = c = 2
        ...     for i in __builtin__.range(1):
        ...         a -= 1
        ...         b += 1''')
        >>> pm = passmanager.PassManager("test")
        >>> res = pm.gather(RangeValues, node)
        >>> res['a']
        Interval(low=-inf, high=2)
        >>> res['b']
        Interval(low=2, high=inf)
        >>> res['c']
        Interval(low=2, high=2)
        """
        assert isinstance(node.target, ast.Name), "For apply on variables."
        if isinstance(node.iter, ast.Call):
            for alias in self.aliases[node.iter.func]:
                if isinstance(alias, Intrinsic):
                    self.add(node.target.id,
                             alias.return_range_content(
                                 [self.visit(n) for n in node.iter.args]))
                else:
                    self.add(node.target.id, UNKNOWN_RANGE)
        else:
            self.add(node.target.id, UNKNOWN_RANGE)

        self.visit_loop(node)

    def visit_loop(self, node):
        """ Handle incremented variables in loop body.

        >>> import gast as ast
        >>> from pythran import passmanager, backend
        >>> node = ast.parse('''
        ... def foo():
        ...     a = b = c = 2
        ...     while a > 0:
        ...         a -= 1
        ...         b += 1''')
        >>> pm = passmanager.PassManager("test")
        >>> res = pm.gather(RangeValues, node)
        >>> res['a']
        Interval(low=-inf, high=2)
        >>> res['b']
        Interval(low=2, high=inf)
        >>> res['c']
        Interval(low=2, high=2)
        """
        old_range = copy.deepcopy(self.result)
        for stmt in node.body:
            self.visit(stmt)
        for name, range_ in old_range.items():
            self.result[name].widen(range_)
        for stmt in node.orelse:
            self.visit(stmt)

    visit_While = visit_loop

    def visit_BoolOp(self, node):
        """ Merge right and left operands ranges.

        TODO : We could exclude some operand with this range information...

        >>> import gast as ast
        >>> from pythran import passmanager, backend
        >>> node = ast.parse('''
        ... def foo():
        ...     a = 2
        ...     c = 3
        ...     d = a or c''')
        >>> pm = passmanager.PassManager("test")
        >>> res = pm.gather(RangeValues, node)
        >>> res['d']
        Interval(low=2, high=3)
        """
        res = list(zip(*[self.visit(elt).bounds() for elt in node.values]))
        return Interval(min(res[0]), max(res[1]))

    def visit_BinOp(self, node):
        """ Combine operands ranges for given operator.

        >>> import gast as ast
        >>> from pythran import passmanager, backend
        >>> node = ast.parse('''
        ... def foo():
        ...     a = 2
        ...     c = 3
        ...     d = a - c''')
        >>> pm = passmanager.PassManager("test")
        >>> res = pm.gather(RangeValues, node)
        >>> res['d']
        Interval(low=-1, high=-1)
        """
        return combine(node.op, self.visit(node.left), self.visit(node.right))

    def visit_UnaryOp(self, node):
        """ Update range with given unary operation.

        >>> import gast as ast
        >>> from pythran import passmanager, backend
        >>> node = ast.parse('''
        ... def foo():
        ...     a = 2
        ...     c = -a
        ...     d = ~a
        ...     f = +a
        ...     e = not a''')
        >>> pm = passmanager.PassManager("test")
        >>> res = pm.gather(RangeValues, node)
        >>> res['f']
        Interval(low=2, high=2)
        >>> res['c']
        Interval(low=-2, high=-2)
        >>> res['d']
        Interval(low=-3, high=-3)
        >>> res['e']
        Interval(low=0, high=1)
        """
        res = self.visit(node.operand)
        if isinstance(node.op, ast.Not):
            return Interval(0, 1)
        elif(isinstance(node.op, ast.Invert) and
             isinstance(res.high, int) and
             isinstance(res.low, int)):
            return Interval(~res.high, ~res.low)
        elif isinstance(node.op, ast.UAdd):
            return res
        elif isinstance(node.op, ast.USub):
            return Interval(-res.high, -res.low)
        else:
            return UNKNOWN_RANGE

    def visit_IfExp(self, node):
        """ Use worst case for both possible values.

        >>> import gast as ast
        >>> from pythran import passmanager, backend
        >>> node = ast.parse('''
        ... def foo():
        ...     a = 2 or 3
        ...     b = 4 or 5
        ...     c = a if a else b''')
        >>> pm = passmanager.PassManager("test")
        >>> res = pm.gather(RangeValues, node)
        >>> res['c']
        Interval(low=2, high=5)
        """
        self.visit(node.test)
        body_res = self.visit(node.body)
        orelse_res = self.visit(node.orelse)
        return orelse_res.union(body_res)

    @staticmethod
    def visit_Compare(_):
        """ Boolean are possible index.

        >>> import gast as ast
        >>> from pythran import passmanager, backend
        >>> node = ast.parse('''
        ... def foo():
        ...     a = 2 or 3
        ...     b = 4 or 5
        ...     c = a < b''')
        >>> pm = passmanager.PassManager("test")
        >>> res = pm.gather(RangeValues, node)
        >>> res['c']
        Interval(low=0, high=1)
        """
        return Interval(0, 1)

    def visit_Call(self, node):
        """ Function calls are not handled for now.

        >>> import gast as ast
        >>> from pythran import passmanager, backend
        >>> node = ast.parse('''
        ... def foo():
        ...     a = __builtin__.range(10)''')
        >>> pm = passmanager.PassManager("test")
        >>> res = pm.gather(RangeValues, node)
        >>> res['a']
        Interval(low=-inf, high=inf)
        """
        result = UNKNOWN_RANGE
        for alias in self.aliases[node.func]:
            if isinstance(alias, Intrinsic):
                alias_range = alias.return_range(
                    [self.visit(n) for n in node.args])
                if result is None:
                    result = alias_range
                else:
                    result.union_update(alias_range)
            else:
                return UNKNOWN_RANGE
        return result

    @staticmethod
    def visit_Num(node):
        """ Handle literals integers values. """
        if isinstance(node.n, int):
            return Interval(node.n, node.n)
        else:
            return UNKNOWN_RANGE

    def visit_Name(self, node):
        """ Get range for parameters for examples or false branching. """
        return self.result[node.id]

    def visit_ExceptHandler(self, node):
        """ Add a range value for exception variable.

        >>> import gast as ast
        >>> from pythran import passmanager, backend
        >>> node = ast.parse('''
        ... def foo():
        ...     try:
        ...         pass
        ...     except __builtin__.RuntimeError as e:
        ...         pass''')
        >>> pm = passmanager.PassManager("test")
        >>> res = pm.gather(RangeValues, node)
        >>> res['e']
        Interval(low=-inf, high=inf)
        """
        if node.name:
            self.result[node.name.id] = UNKNOWN_RANGE
        for stmt in node.body:
            self.visit(stmt)

    def generic_visit(self, node):
        """ Other nodes are not known and range value neither. """
        super(RangeValues, self).generic_visit(node)
        return UNKNOWN_RANGE
