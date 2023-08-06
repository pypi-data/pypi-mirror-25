# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function


def choice_add_all(code=None, text=None):
    """为choice 添加全部选择项"""

    code = code or '*'
    text = text or '全部'

    def _choice_add_all(fn):
        @functools.wraps(fn)
        def __choice_add_all(*args, **kwargs):
            result = fn(*args, **kwargs)
            if kwargs.get('is_all', True):
                result.insert(0, (code, text))
            return result
        return __choice_add_all
    return _choice_add_all