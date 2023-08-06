# -*- coding:utf-8 -*-
"""
@author:bbw
@file:nester.py
@time:2017/10/9  10:08
"""
"""这个模块提供了一个函数，打印列表，其中可能包含（也可能不包含嵌套列表）"""
def print_lol(the_list, level):
    """这个函数取一个位置参数，名为the list，可以是任何python列表，所指定的每个数据项会递归的显示到屏幕上，且各占一行.
        第二个参数用来在遇到嵌套列表时插入制表符"""

    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
                print("\t", end='')
            print(each_item)

