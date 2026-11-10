# Topic: Python decorators

### Simple Explanation

Python decorators are a powerful tool for modifying the behavior of functions without changing their source code. They allow you to wrap a function with another function, which is called the decorator, without altering the original function's name or syntax. This technique is useful for tasks such as logging, authentication, and caching.

Decorators are named after the word "decorate", implying that they add a new layer of functionality to an existing function. Think of a decorator as a layer of frosting on a cake – it doesn't change the cake itself, but it adds a new flavor and texture.

Python decorators are a fundamental concept in functional programming and are widely used in the Python community.

### Key Concepts

- **Function wrapper**: a function that takes another function as an argument and returns a new function that "wraps" the original function.
- **Decorator syntax**: `@decorator_name(func_name)` or `def decorator_name(func_name): ...`
- **Decorator arguments**: a list of arguments passed to the decorator, which can be accessed using the `*args` and `**kwargs` syntax.
- **Decorator return value**: the value returned by the decorator, which is used to modify the behavior of the original function.

### Example

```python
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")

say_hello()
```

The output will be:
```
Something is happening before the function is called.
Hello!
Something is happening after the function is called.
```

## Practice Exercise
- **Task**: write a decorator that logs the execution time of a function.
- **Expected input**: None
- **Expected output**: a Python function that can be used as a decorator.
- **Hint 1**: use the `time` module to measure execution time.
- **Hint 2**: use the `functools.wraps` decorator to preserve the original function's metadata.

## Common Mistakes
* Using `@decorator_name` with a function name instead of a decorator function.
* Forgetting to use `functools.wraps` to preserve the original function's metadata.
* Not handling exceptions properly in the decorator.

## Review Comments
- **Missing information**: The study guide could benefit from a clear explanation of how decorators are used with classes and object-oriented programming.
- **Unclear parts**: The explanation of the decorator return value is not clear.
- **Suggestions**:
  - Improve the explanation of the decorator return value to explain how it is used to modify the behavior of the original function.
  - Add more details about how to handle exceptions in the decorator.
  - Clarify the difference between `*args` and `**kwargs` in the context of decorator arguments.
- **Recommendation**: Needs revision

## Final Summary
Students should remember that decorators are a powerful tool for modifying function behavior without changing source code, and that they can be used to add features such as logging, authentication, and caching to existing functions. They should also understand how to use decorators with classes and object-oriented programming, and how to handle exceptions and access decorator arguments.
