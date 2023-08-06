# -*- coding: UTF-8 -*-
from __future__ import absolute_import, unicode_literals, print_function


class Library(object):
    def __init__(self):
        self.filters = {}
        self.tags = {}

    def tag(self, name=None, compile_function=None):
        if name is None and compile_function is None:
            return self.tag_function
        elif name is not None and compile_function is None:
            if callable(name):
                return self.tag_function(name)
            else:
                def dec(func):
                    return self.tag(name, func)

                return dec
        elif name is not None and compile_function is not None:
            self.tags[name] = compile_function
            return compile_function
        else:
            raise ValueError(
                "Unsupported arguments to Library.tag: (%r, %r)" % (
                    name, compile_function
                )
            )

    def tag_function(self, func):
        self.tags[getattr(func, "_decorated_function", func).__name__] = func
        return func

    def filter(self, name=None, filter_func=None, **flags):
        """
        Register a callable as a template filter. Example:

        @register.filter
        def lower(value):
            return value.lower()
        """
        if name is None and filter_func is None:
            # @register.filter()
            def dec(func):
                return self.filter_function(func, **flags)

            return dec
        elif name is not None and filter_func is None:
            if callable(name):
                # @register.filter
                return self.filter_function(name, **flags)
            else:
                # @register.filter('somename') or @register.filter(name='somename')
                def dec(func):
                    return self.filter(name, func, **flags)

                return dec
        elif name is not None and filter_func is not None:
            # register.filter('somename', somefunc)
            self.filters[name] = filter_func
            for attr in ('expects_localtime', 'is_safe', 'needs_autoescape'):
                if attr in flags:
                    value = flags[attr]
                    # set the flag on the filter for FilterExpression.resolve
                    setattr(filter_func, attr, value)
                    # set the flag on the innermost decorated function
                    # for decorators that need it, e.g. stringfilter
                    if hasattr(filter_func, "_decorated_function"):
                        setattr(filter_func._decorated_function, attr, value)
            filter_func._filter_name = name
            return filter_func
        else:
            raise ValueError(
                "Unsupported arguments to Library.filter: (%r, %r)" %
                (name, filter_func),
            )

    def filter_function(self, func, **flags):
        name = getattr(func, "_decorated_function", func).__name__
        return self.filter(name, func, **flags)

