#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-08-28 16:20
# @Author  : hys
# @Site    : 
# @File    : hys.py
# @Software: PyCharm
# @Desc     :
# @license : Copyright(C), Your Company
# @Contact : george.zw513@gmail.com
import datetime


class Hys:
    """本类主要用于描述介绍自己"""
    def __init__(self):
        self.name = "赵建宏"
        self.sex = "男"
        self.age = 0
        self.high = "165cm"
        self.weight = "55Kg"


if __name__ == "__main__":
    print("当前模块测试")
    nd = datetime.datetime.today()
    print(nd)

