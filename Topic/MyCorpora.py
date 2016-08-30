#!/usr/bin/python
#encoding=utf-8
#Script Name :MyCorpora.py
#Author : Simon Shi
#created : 2016.08.29
#Version : 1.0
#Description : 对文本库中文本做转换操作

import os,gensim,codecs

class MyCorpora(object):
    documents = []
    stopWords = []
    def __init__(self):
        self.documents = []
        self.stopWords = []

    def turnToList(self,filename):
        fileObject = codecs.open(os.path.abspath('..\\Source')+"\\"+filename,'rU',encoding='utf-8')
        self.documents =[line.strip() for line in fileObject.readlines()]
        fileObject.close()
        return self.documents
    def useStopWords(self,stopWordListName):
        fileObject = codecs.open(os.path.abspath('..\\Source')+'\\'+stopWordListName,'rU',encoding='utf-8')
        self.stopWords = [line.strip() for line in fileObject.readlines()]
        return self.stopWords
    def getVector(self):

