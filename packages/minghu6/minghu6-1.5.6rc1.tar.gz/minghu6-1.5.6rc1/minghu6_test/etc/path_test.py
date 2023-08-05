# -*- coding:utf-8 -*-
# !/usr/bin/env python3

"""

"""


def test_add_postfix():
    from minghu6.etc.path import add_postfix

    fn = 'hello.py'
    postfix = 'test'

    new_name = add_postfix(add_postfix(fn, postfix), postfix)
    assert new_name == 'hello_test_test.py', new_name

    fn = 'c:\\coding\\hello.py'
    postfix = 'test'
    new_name = add_postfix(fn, postfix)
    assert new_name == 'c:\\coding\\hello_test.py'

    new_name = add_postfix('hello', 'test')
    assert new_name == 'hello_test'


def test_get_cwd_preDir():
    # print(path.get_cwd_preDir(2))
    pass


if __name__ == '__main__':
    test_add_postfix()
    test_get_cwd_preDir()
