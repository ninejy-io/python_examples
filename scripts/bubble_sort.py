# -*- coding: utf-8 -*-


def bubble_sort(li):
    print('begin:', li)
    n = len(li)
    for i in range(0, n):
        count = 0
        for j in range(0, n-1-i):
            if li[j] > li[j+1]:
                li[j], li[j+1] = li[j+1], li[j]
                count += 1
        if count == 0:
            break
        print('count:', count)
    print('end:', li)


a = [3, 900, 2, 4, 1, 6, 7, 8, 34, 22, 55, 10, 200, 56, 89, 93, 23, 44, 36, 67, 192, 4000, 298, 322]

bubble_sort(a)
