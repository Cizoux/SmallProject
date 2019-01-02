#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pyocr
import importlib
import sys
importlib.reload(sys)
import time 
import os
import re

import xlwt #写入文件
import xlrd #打开excel文件
 
PATTERN1 = r'募集说明书'
PATTERN2 = r'联系人'

pattern1 = re.compile(PATTERN1)
pattern2 = re.compile(PATTERN2)

text_path = r'D:\guanlan\xianqi_spider\xianqi_spider\xianqi_spider\test\file\中交一公局集团有限公司注册文件补充信息的函.txt'
 
def extract(filename):
    # text_path = r'D:\guanlan\xianqi_spider\xianqi_spider\xianqi_spider\test\file\'+ filename
    f = open(filename)
    lines = f.readlines(5000)
    start = 0
    end = 0
    print('start')
    for i in range(len(lines)):
        # print(lines[i])
        if pattern1.search(lines[i]):
            # print(lines[i])
            start = i
        if pattern2.search(lines[i]):
            end = i
            # print(lines[i])
    f.close()
    print(start)
    print(end)
    if start is not None and end is not None:
        return lines[0],lines[start:end]
    else:
        return lines[0],'0'


if __name__ == '__main__':
    # extract(text_path)
    path = r'D:\guanlan\xianqi_spider\xianqi_spider\xianqi_spider\test\file'
    excelfile = xlwt.Workbook(encoding='utf-8',style_compression=0)
    sheet = excelfile.add_sheet('data')
    files = os.listdir(path)
   
    for i in range(len(files)):
        print(files[i])
        file_path = os.path.join(path,files[i])
        company,data = extract(file_path)
        sheet.write(i,0,company)
        sheet.write(i,1,data)
        excelfile.save('company.xls')