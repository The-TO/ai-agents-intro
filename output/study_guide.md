# Topic: Python decorators

### Simple Explanation
Python decorators are a powerful tool in Python programming that allows you to modify or extend the behavior of a function without permanently changing it. In essence, a decorator is a small function that takes another function as an argument and returns a new function that "wraps" the original function. This allows you to add new functionality to an existing function without altering its source code.

Decorators are often used for tasks such as logging, authentication, or caching, but they can be used for any kind of function modification. They are a key feature of the Python programming language and are widely used in many areas of software development.

In the context of Python, decorators are implemented using the `@` symbol, which is used to indicate that a function is a decorator. For example, `@my_decorator` is equivalent to `my_function = my_decorator(my_function)`.

### Key Concepts
- **Decorator**: A small function that takes another function as an argument and returns a new function that wraps the original function.
- **Wrapper function**: A new function that is created by a decorator and returns the result of the original function.
- **Function wrapping**: The process of adding new functionality to an existing function without permanently changing its source code.

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
This code defines a decorator `my_decorator` that takes a function `func` as an argument and returns a new function `wrapper`. The `wrapper` function calls the original `func` and adds some additional behavior before and after the call. The `@my_decorator` syntax is used to apply the decorator to the `say_hello` function, effectively creating a new function `wrapper` that wraps the original `say_hello` function.

## Practice Exercise
- **Task**: Implement a simple decorator that prints a message before and after the execution of a function.
- **Expected input**: None
- **Expected output**: The output of the decorated function.
- **Hint 1**: Use the `@` symbol to apply the decorator to a function.
- **Hint 2**: Use the `print` function to add the desired behavior.

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

## Common Mistakes
* **Overcomplicating the decorator**: Avoid using the decorator for tasks that can be achieved with a simple function call or a loop.
* **Forgetting to return the original function**: Ensure that the decorator returns the original function to maintain the correct function signature.
* **Not handling potential errors**: Add error handling code to your decorator to ensure it can handle any exceptions that might occur during function execution.
