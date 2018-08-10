#!/usr/bin/env python
# coding: utf-8
import csv
from openpyxl import Workbook

# def csv_to_xlsx(csv_name, excel_name):
    # import xlwt
#     with open(csv_name, 'r', encoding='utf-8') as f:
#         read = csv.reader(f)
#         workbook = xlwt.Workbook()
#         sheet = workbook.add_sheet('data')
#         l = 0
#         for line in read:
#             # print(line)
#             r = 0
#             for i in line:
#                 # print(i)
#                 sheet.write(l, r, i)
#                 r += 1
#             l += 1

#     workbook.save(excel_name)


def csv_to_xlsx(csv_name, excel_name):
    workbook = Workbook()
    sheet = workbook.active

    with open(csv_name, 'r', encoding='utf-8') as f:
        read = csv.reader(f)
        for row in read:
            sheet.append(row)

    workbook.save(excel_name)


if __name__ == '__main__':
    import sys
    c = sys.argv[1]
    e = sys.argv[2]
    csv_to_xlsx(c, e)
