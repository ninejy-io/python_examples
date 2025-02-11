### Python垃圾回收

- 引用计数器
- 标记清除
- 分代回收
- 缓存机制

#### 1. 引用计数器

###### 1.1 环状双向链表 refchain

- 在Python程序中创建的任何对象都会放在refchain双向链表中

  ```python
  # 内部会创建一些数据 [ 上一个对象, 下一个对象, 类型, 引用个数, val='张三' ]
  name = "张三"
  
  # 内部会创建一些数据 [ 上一个对象, 下一个对象, 类型, 引用个数, items=元素, 元素个数 ]
  name = [ 'aa', 'bb' ]
  ```

  在C源码中如何体现每个对象中都有的相同的值: PyObject结构体(4个值)

  有多个元素组成的对象: PyObject结构体(4个值) + ob_size

###### 1.2 类型结构体封装

- ```
  data = 3.14
  # 内部创建
  	_ob_next = refchain中的下一个对象
  	_ob_prev = refchain中的上一个对象
  	ob_refcnt = 1
  	ob_type float
  	ob_fval = 3.14
  ```


###### 1.3 引用计数器

​	当python程序运行时，会根据数据类型的不同找到对应的结构体，根据结构体中的字段来进行创建相关的数据，然后将对象加到refchain双向链表中。

​	在C源码中有两个关键的结构体: PyObject、PyVarObject

​	每个对象中有ob_refcnt就是引用计数器，默认值为1，当有其他变量引用对象时，引用计数器就会发生变化。

​	当一个对象的引用计数器为0时，意味着没有人使用这个对象了，这个对象就是垃圾，垃圾回收。

​	回收: 1. 对象从refchain链表中移除  2. 将对象销毁，内存回收

###### 1.4 循环引用

```python
v1 = [1,2,3]  # v1 refcnt = 1
v2 = [4,5,6]  # v2 refcnt = 1
v1.append(v2)  # v2 refcnt = 2
v2.append(v1)  # v1 refcnt = 2
del v1  # v1 refcnf = 1
del v2  # v2 refcnt = 1
```

#### 2. 标记清除

目的: 为了解决引用计数器循环引用的不足。

实现: 在python的底层 再 维护一个链表, 专门放那些可能存在循环引用的对象(list/tuple/dict/set)。

在python内部 `某种情况`下触发，会去扫描 可能存在循环引用的链表中的每个元素，如果有则让双方引用计数器-1，如果是0则垃圾回收。

问题:

- 什么时候扫描？
- 可能存在循环引用的链表扫描代价大，每次扫描耗时久。

#### 3. 分代回收

将有可能存在循环引用的对象维护成三个链表

- 0代: 0代中对象个数达到700个扫描一次

- 1代: 0代扫描10次，则1代扫描一次

- 2代: 1代扫描10次，则2代扫描一次


#### 4. Python缓存

###### 4.1 池 （int/字符串）

为了避免重复创建和销毁一些常见对象，维护池。

```python
# 启动解释器时，Python内部帮我们创建: -5, -4, -3, ... 257
v1 = 7 # 内部不会开辟内存，直接去池中获取
v2 = 9 # 内部不会开辟内存，直接去池中获取
v3 = 9 # 内部不会开辟内存，直接去池中获取
print(id(v2), id(v3))
```

###### 4.2 free_list (float/list/tuple/dict)

当一个对象的引用计数器为0时，按理说应该回收，内部不会直接回收，而是将对象添加到 free_list 链表中当缓存。以后再去创建对象时，不再重新开辟内存，而是直接使用 free_list 。

```python
v1 = 3.14  # 开辟内存，内部存储结构体中定义那几个值，并存到 refchain 中
del v1  # refchain 中移除，将对象添加到 free_list 中(80个)，free_list 满了则销毁
v2 = 99.99  # 不会重新开辟新内存，去 free_list 中获取对象，对象内部数据初始化，再放到 refchain 中
```

