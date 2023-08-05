# -*- coding: utf-8 -*-


def class_loader(name):
    '''
    Imports and returns given class/func/variable/module name

    Args:
        name: A string of what to import ex. foo.bar.MyClass

    Returns:
        class/func/variable/module
    '''
    components = name.split('.')
    mod = __import__(components[0])

    for comp in components[1:]:
        mod = getattr(mod, comp)

    return mod
