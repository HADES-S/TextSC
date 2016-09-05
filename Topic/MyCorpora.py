#!/usr/bin/python
#encoding=utf-8
#Script Name :MyCorpora.py
#Author : Simon Shi
#created : 2016.08.29
#Version : 1.0
#Description : 对文本库中文本做转换操作

import os,gensim,codecs
from collections import defaultdict
from pprint import pprint

from Topic.nlpir import getSegmentationWords

project_path = os.getcwd()
project_path = project_path[:project_path.find("TextSC")+6]

class MyCorpora(object):
    documents = []
    stopWords = []
    vector = []
    def __init__(self,documentFileName,stopWordsFileName):
        self.turnToList(documentFileName)
        self.useStopWords(stopWordsFileName)


    #提取文本中的文档类
    def turnToList(self,filename):
        fileObject = codecs.open(project_path+"\\Source"+"\\"+filename,'rU',encoding='utf-8')
        self.documents = [line.strip() for line in fileObject.readlines()]
        fileObject.close()
        return self.documents

    #去除停用词的部分
    def useStopWords(self,stopWordListName):
        fileObject = codecs.open(project_path+"\\Source"+'\\'+stopWordListName,'rU',encoding='utf-8')
        self.stopWords = [line.strip() for line in fileObject.readlines()]
        return self.stopWords

    def getVector(self):
        splitdocuments = []
        for sentence in self.documents:
            splitdocuments.append(getSegmentationWords(sentence.encode('utf-8')))
        texts = [[word for word in document if word.decode('utf-8') not in self.stopWords] for document in splitdocuments]
        frequency =defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token]+=1
        texts = [[token for token in text if frequency[token] > 1]
                 for text in texts]
        dictionary = gensim.corpora.Dictionary(texts)
        if(not os.path.exists(project_path+"//Source//tmp")):
            os.makedirs(project_path+"//Source//tmp")
        dictionary.save(project_path+"//Source//tmp//deerwester.dict")
        corpus = [dictionary.doc2bow(text) for text in texts]
        gensim.corpora.MmCorpus.serialize(project_path+'//Source//tmp//deerwester.mm',corpus)
        return corpus
    def convertQuery(self,sentence):
        sentence =getSegmentationWords(sentence.encode('utf-8'))
        texts = [ word for word in sentence if word.decode('utf-8') not in self.stopWords]
        return texts


