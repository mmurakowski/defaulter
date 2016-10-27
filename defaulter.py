__doc__ = """
Radically change the behavior of default arguments.

Before:

    >>> def foo(a=[]):
    ...     a.append(1)
    ...     return a
    ... 
    >>> foo()
    [1]
    >>> foo()
    [1, 1]

After:

    >>> import defaulter
    >>> @defaulter
    ... def foo(a=[]):
    ...     a.append(1)
    ...     return a
    ... 
    >>> foo()
    [1]
    >>> foo()
    [1]

Enjoy!
"""
import sys, types

class _defaulter(types.ModuleType):
    def _get_closure_vars(self, f):
        return dict(zip(f.__code__.co_freevars, [c.cell_contents for c in f.__closure__ or []]))
    
    def _get_globals(self, f):
        return dict(f.__globals__, **self._get_closure_vars(f))

    def __call__(self, f):
        import inspect, ast, textwrap, functools, sys
        
        source = textwrap.dedent(inspect.getsource(f))
        a = ast.parse(source)
        default_args = tuple(compile(ast.Expression(d), filename='<ast>', mode='eval')
                             for d in a.body[0].args.defaults)
       
        func_globals = self._get_globals(f)
        func_locals = sys._getframe(1).f_locals
       
        @functools.wraps(f)
        def inner(*args, **kwargs):
            f.__defaults__ = tuple(eval(e, func_globals, func_locals) for e in default_args)
            return f(*args, **kwargs)
       
        return inner

sys.modules[__name__] = _defaulter('defaulter', __doc__)
