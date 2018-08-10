# coding: utf-8
import time

# 原函数带参数的装饰器
def timer(func):
    def inner(*args, **kwargs):
        print('do something before')
        start = time.time()
        ret = func(*args, **kwargs)
        print('do something after')
        end = time.time()
        print(end - start)
        return ret
    return inner


# @timer
# def func1(a, b):
#     print('in func1')
#     print(a, b)
# func1(1, 2)


# @timer
# def func2(a):
#     print('in func2 and get a: %s' % (a))
#     return 'func2 over'
# func2('bbbbbbbbb')
# print(func2('aaaaaa'))


# 带参数的装饰器
def  outer(flag=True):
    def wrapper(func):
        def inner(*args, **kwargs):
            if flag:
                print('before')
                ret = func(*args, **kwargs)
                print('after')
            else:
                ret = func(*args, **kwargs)
            return ret
        return inner
    return wrapper

# @outer(False)
# def func3():
#     print('I am func3')
# func3()


# 多个装饰器装饰一个函数
def wrapper1(func):
    def inner(*args, **kwargs):
        print('wrapper1 before')
        ret = func(*args, **kwargs)
        print('wrapper1 after')
        return ret
    return inner


def wrapper2(func):
    def inner(*args, **kwargs):
        print('wrapper2 before')
        ret = func(*args, **kwargs)
        print('wrapper2 after')
        return ret
    return inner


@wrapper1
@wrapper2
def func5():
    print('I am func5')
func5()
