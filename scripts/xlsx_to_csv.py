#!/usr/bin/env python
# coding: utf-8
import xlrd
import csv
import codecs


def xlsx_to_csv(excel_name, csv_name):
    workbook = xlrd.open_workbook(excel_name)
    table = workbook.sheet_by_index(0)
    with codecs.open(csv_name, 'w', encoding='utf-8') as f:
        write = csv.writer(f)
        for i in range(table.nrows):
            value = table.row_values(i)
            write.writerow(value)


if __name__ == '__main__':
    import sys
    e = sys.argv[1]
    c = sys.argv[2]
    xlsx_to_csv(e, c)
