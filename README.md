## Let's talk about default args
What does the following code output?
```python
def foo(a=[]):
    a.append(1)
    return a
print(foo())
print(foo())
```
If you've never been bitten by using mutable default args in a function, it might surprise you to learn that the list object ```a=[]``` is only instantiated once, at function definition time, and is then carried around by the function object. Then, if you mutate it, the mutated version is what's used as the default in all subsequent calls. Therefore, the code outputs
```python
[1]
[1, 1]
```
The usual solution is to move the instantiation into the function body, i.e. do something like
```python
def foo(a=None):
    if a is None:
        a = []
    ...
```
or, if ```None``` is a valid input,
```python
_SENTINEL = object()
def foo(a=_SENTINEL):
    if a is _SENTINEL:
        a = []
    ...
```
but that obfuscates the code unnecessarily. Let's try to do better.

## Defaulter
defaulter.py re-evaluates the function default arguments at call-time, letting you use mutable objects without worry.
```python
import defaulter

@defaulter
def foo(a=[]):
    a.append(1)
    return a
print(foo()) # [1]
print(foo()) # [1]
```
defaulter.py works with any default comprised of a python literal, literal-expression, or function call. Want to see the time taken in a function?
```python
import defaulter, datetime
@defaulter
def long_running_function(start_time=datetime.datetime.now(), ...):
   ...
   time_taken = datetime.datetime.now() - start_time
```

Just don't get too cute:
```python
import defaulter
some_var = []

@defaulter
def foo(a=some_var):
    a.append(1)
    return a
print(foo()) # [1]
print(foo()) # [1, 1]
```
Also, obviously, never actually use this.

