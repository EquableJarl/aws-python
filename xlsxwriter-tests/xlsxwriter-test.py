#!/usr/bin/env python3

import xlsxwriter

workbook = xlsxwriter.Workbook('hello.xlsx')
worksheet = workbook.add_worksheet()

cell_format = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color' : 'gray'})

headers = ['ami-id', 'platform', 'ami-name']

for count, value in enumerate(headers):
    worksheet.write(0, count, value, cell_format)

workbook.close()

