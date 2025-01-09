
def ca_add_common_doc(doc: str):
    """
    Decorator to append a common documentation string to the docstring of a function.
    :param doc: The documentation string to append.
    :return: A decorator function that appends doc to the __doc__ attribute of the target function.
    """
    def decorator(func):
        func.__doc__ = (func.__doc__ or "") + doc
        return func
    return decorator