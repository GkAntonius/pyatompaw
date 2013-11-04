
import sys

def set_child_function(parent_cls, child_name, child_cls, func_name):
    """
    Create a parent function which calls a child function. 

    Arguments:
        parent_cls:
            The class which will recieve a function.
        child_name:
            The child name within the parent namespace.
        child_cls:
            The child class.
        func_name:
            The function name.
    """

    child_function = getattr(child_cls, func_name)

    def parent_function(parent, *args, **kwargs):
        child = getattr(parent, child_name)
        child_func = getattr(child, func_name)
        try:
            return child_func(*args, **kwargs)
        except Exception as E:
            type, value, traceback = sys.exc_info()
            message = child_cls.__name__ + '.' + func_name + ': ' + E.message
            raise Exception, (message, type), traceback

    parent_function.func_doc = child_function.func_doc
    parent_function.func_name = child_function.func_name

    setattr(parent_cls, func_name, parent_function)


def set_child_functions(cls, child_name, child_cls):
    """
    Use the child's "_to_parent_functions" attribute
    to set the children functions.
    """
    for function in child_cls._to_parent_functions:
        set_child_function(cls, child_name, child_cls, function)


def set_child_property(parent_cls, child_name, child_cls, prop_name):
    def getter(self):
        child = getattr(self, child_name)
        return getattr(child, prop_name)
    def setter(self, val):
        child = getattr(self, child_name)
        return setattr(child, prop_name, val)
    setattr(parent_cls, prop_name, property(getter, setter))


def set_child_properties(cls, child_name, child_cls):
    """
    Use the child's "_to_parent_properties" attribute
    to set the children functions.
    """
    for prop in child_cls._to_parent_properties:
        set_child_property(cls, child_name, child_cls, prop)
