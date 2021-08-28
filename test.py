from typing import Callable

def yeet(func: Callable):
    def wrapper(*args, **kwargs):
        val = func(*args, **kwargs)
        return val
    print(f"YEET")
    return wrapper

def hello(func: Callable):
    def wrapper(*args, **kwargs):
        val = func(*args, **kwargs)
        return val
    print('HELLOO')
    return wrapper

@yeet
@hello
def testing(text):
    print(text)

testing('ok')