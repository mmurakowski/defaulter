import defaulter

def test_expression():
    def foo(a=object()):
        return a
    # base case
    assert foo() is foo()
    
    foo = defaulter(foo)
    # magic
    assert foo() is not foo()

def test_closure():
    o = 2
    def outer():
        x = 2
        y = [1]
        def inner(a=o*x*y):
            # no magic; you need to reference them to get the closure :(
            [o,x,y]
            a.append(1)
            return a
        return inner
    
    foo = outer()
    # base case
    assert foo() == 5*[1]
    assert foo() == 6*[1]

    foo = defaulter(foo)
    # magic!
    assert foo() == 5*[1]
    assert foo() == 5*[1]

def test_closure_magic():
    o = 2
    def outer():
        x = 2
        y = [1]
        @defaulter
        def inner(a=o*x*y):
            a.append(1)
            return a
        return inner
    
    foo = outer()
    assert foo() == 5*[1]
    assert foo() == 5*[1]
