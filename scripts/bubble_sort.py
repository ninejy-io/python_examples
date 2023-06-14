# coding: utf-8

lis = [3, 9, 22, 1, 23, 19, 15, 27, 8, 6]


def select_sort(arr: list):
    length = len(arr)
    if length <= 1:
        return arr[0]
    else:
        for i in range(length-1):
            min_index = i
            for j in range(i+1, length):
                if arr[min_index] > arr[j]: # 找出最小值
                    min_index = j

            if i != min_index:
                arr[i], arr[min_index] = arr[min_index], arr[i]

        return arr


def bubble_sort(arr: list):
    length = len(arr)
    if length <= 1:
        return arr
    else:
        for i in range(length-1):
            need_exchange = False
            for j in range(length-i-1):
                if arr[j] > arr[j+1]: # 每次循环把小的放左侧
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    need_exchange = True

            if not need_exchange:
                break

        return arr


# print(select_sort(lis))
print(bubble_sort(lis))
