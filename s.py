from file_loading_tests import load_config_file

import sys, re


# with open("config.txt", "r") as f:
#     config = f.read()
#     print(config)


# print("yes"if re.match(r"^Frame: .*\nWater: .*\nWood: .*\nFood: .*\nGold: (.)*", config) else "no")
# print("")
# print("hi")

# def devide(a, b):
#     if b == 0:
#         raise ValueError
#     return a / b
#
#
# class InputError(Exception):
#     # 自定义异常类型的初始化
#     def __init__(self, value):
#         self.value = value
#
#     # 返回异常类对象的说明信息
#     def __str__(self):
#         return ("{} is invalid input".format(repr(self.value)))

class A(object):
    def __init__(self, f):
        self.name = f


a = A(2)
b = A(1)
print(a == b)
# b = A("1)
# print(a,b)
# print(a._A__a())


# print("12345" + str(A("aas")))
