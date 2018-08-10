# coding: utf-8
'''
单例模式的4种实现方式
'''

'''
1. 使用模块
直接在其他文件中导入该对象
'''
# class Singleton(object):
#     def foo():
#         pass
# singleton = Singleton()


'''
2. 使用类
'''
# import time
# import threading


# class Singleton(object):
#     _instance_lock = threading.Lock()

#     def __init__(self):
#         time.sleep(1)

#     @classmethod
#     def instance(cls, *args, **kwargs):
#         if not hasattr(Singleton, '_instance'):
#             with Singleton._instance_lock:
#                 if not hasattr(Singleton, '_instance'):
#                     Singleton._instance = Singleton(*args, **kwargs)
#         return Singleton._instance


# def task(arg):
#     obj = Singleton.instance()
#     print(obj)


# for i in range(10):
#     t = threading.Thread(target=task, args=[i,])
#     t.start()

# time.sleep(20)
# obj = Singleton.instance()
# print(obj)


'''
基于__new__方法
'''
# import threading


# class Singleton(object):
#     _instance_lock = threading.Lock()

#     def __init__(self):
#         pass

#     def __new__(cls, *args, **kwargs):
#         if not hasattr(Singleton, '_instance'):
#             with Singleton._instance_lock:
#                 if not hasattr(Singleton, '_instance'):
#                     Singleton._instance = object.__new__(cls)
#         return Singleton._instance


# def task(arg):
#     obj = Singleton()
#     print(obj)


# obj1 = Singleton()
# obj2 = Singleton()
# print(obj1, obj2)


# for i in range(10):
#     t = threading.Thread(target=task, args=[i,])
#     t.start()


'''
基于metaclass
'''
import threading


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with SingletonType._instance_lock:
                if not hasattr(cls, '_instance'):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance


class Foo(object):
    '''
    Python3
    class Foo(metaclass=SingletonType):
        pass
    '''
    __metaclass__ = SingletonType

    def __init__(self, name):
        self.name = name


obj1 = Foo('name')
obj2 = Foo('name')
print(obj1, obj2)

