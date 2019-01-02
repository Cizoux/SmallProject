#!/usr/bin/python
#coding=utf-8
import time
import json
# from xianqi_spider.items import XianqiSpiderItem
import requests
import scrapy
import urllib
import re

import pyocr
import importlib
import sys
import time
 
importlib.reload(sys)
 
import os.path
from pdfminer.pdfparser import  PDFParser,PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal,LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed


PATTERN = '[a-zA-Z0-9_\u4e00-\u9fa5\()\.*]{3,100}?(?:的函)'
pattern = re.compile(PATTERN)

def getFile(url,file_name): 
    u = urllib.request.urlopen(url) 
    f = open(file_name, 'wb')
    block_sz = 8192 
    while True: 
        buffer = u.read(block_sz) 
        if not buffer: 
            print('no buffer')
            break 
        f.write(buffer)
    print('download successful')       
    f.close() 

def parse(text_path,regFileName):
    '''解析PDF文本，并保存到TXT文件中'''
    fp = open(text_path,'rb')
    txt_name = text_path.split('.')[0]+'.txt'
    try:
        #用文件对象创建一个PDF文档分析器
        parser = PDFParser(fp)
        #创建一个PDF文档
        doc = PDFDocument()
        #连接分析器，与文档对象
        parser.set_document(doc)
        doc.set_parser(parser)
        
        #提供初始化密码，如果没有密码，就创建一个空的字符串
        doc.initialize()
        #检测文档是否提供txt转换，不提供就忽略
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
            with open(txt_name,'a') as f:
                f.write(regFileName  +"\n")
            #创建PDF，资源管理器，来共享资源
            rsrcmgr = PDFResourceManager()
            #创建一个PDF设备对象
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr,laparams=laparams)
            #创建一个PDF解释其对象
            interpreter = PDFPageInterpreter(rsrcmgr,device)
            #循环遍历列表，每次处理一个page内容
            # doc.get_pages() 获取page列表
            for page in doc.get_pages():
                interpreter.process_page(page)
                    #接受该页面的LTPage对象
                layout = device.get_result()
                    # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
                    # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
                    # 想要获取文本就获得对象的text属性，
                for x in layout:
                    if(isinstance(x,LTTextBoxHorizontal)):
                        with open(txt_name,'a') as f:
                            results = x.get_text()
                            results.replace(u'\xb3 ', u' ')
                            results = "".join(results.split())
                                # print(results)
                            f.write(results  +"\n")
    except:
        print('a oh')

base_url = 'http://zhuce.nafmii.org.cn/fans/publicQuery/detail?instNo={}&projTrackNo={}&releaseTitle=undefined'
search_url = 'http://zhuce.nafmii.org.cn/fans/publicQuery/releFileProjDataGrid'
fileid_url = 'http://zhuce.nafmii.org.cn/fans/publicQuery/feedBackGrid?instNo={0}&projTrackNo={1}'

response = requests.get(search_url).json()
datas = response['rows']
# print(datas)
# print(datas)
for i in range(1831,2635):
    data = datas[i]
    # print(len(datas))
    print(i)
    item = {}
    item['instNo'] = data['instNo']
    item['leadManagerStatus'] = data['leadManagerStatus'] 
    item['projTrackNo'] = data['projTrackNo']
    item['regFileName'] = data['regFileName']

    item['releaseTime'] = data['releaseTime']
    print(item['releaseTime'])
    if item['releaseTime'] < '2018-12-31' and item['releaseTime'] > '2018-01-01' :
        if item['leadManagerStatus'] == '6010':
            print(item['regFileName'])
            url = fileid_url.format(item['instNo'], item['projTrackNo'])
            fileid_datas = requests.get(url).json()
            # print(fileid_datas)
            fileid_data = fileid_datas['rows']
            for pdf in fileid_data: 
                # pdfname = pdf['fileName'].split('.')[0]
                # exist = pattern.search(pdfname)
                if True:
                    # print(exist.group(0))
                    item['storeLocation'] = pdf['storeLocation']
                    item['fileName'] = pdf['fileName']
                    nopdf = item['fileName'].split('.')[0]
                    file_name = urllib.parse.quote(nopdf)
                    file_url = 'http://zhuce.nafmii.org.cn/file_web/file/download?bo=%7B%22fileName%22%3A%22'+file_name+'.pdf%22%2C%22fileId%22%3A%22'+item['storeLocation']+'%22%7D'
                    # file_url.format(item['storeLocation'])
                    # print(file_url)
                    getFile(file_url,item['fileName'])
                    # parse(item['fileName'],item['regFileName'])

# data = '关于张家港保税区金港资产经营有限公司注册文件补充信息的函的回函(2018年09月19日12时16分39秒).pdf'
# data = data.split('.')[0]
# # print(data)

# m = pattern.search(data)
# if m is not None:
#     print(m.group(0))
# # def ifmatch(name):