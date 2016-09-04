#!/usr/bin/python
#encoding=utf-8
#Script Name :MyCorpora.py
#Author : Simon Shi
#created : 2016.08.29
#Version : 1.0
#Description : 对文本库中文本做转换操作

import os,gensim,codecs
import nlpir
from collections import defaultdict
from pprint import pprint

class MyCorpora(object):
    documents = []
    stopWords = []
    vector = []
    def __init__(self,documentFileName,stopWordsFileName):
        self.turnToList(documentFileName)
        self.useStopWords(stopWordsFileName)


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
        splitdocuments = []
        for sentence in self.documents:
            splitdocuments.append(nlpir.getSegmentationWords(sentence.encode('utf-8')))
        texts = [[word for word in document if word.decode('utf-8') not in self.stopWords] for document in splitdocuments]
        frequency =defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token]+=1
        texts = [[token for token in text if frequency[token] > 1]
                 for text in texts]
        dictionary = gensim.corpora.Dictionary(texts)
        if(not os.path.exists("../Source/tmp")):
            os.makedirs("../Source/tmp")
        dictionary.save("../Source/tmp/deerwester.dict")
        corpus = [dictionary.doc2bow(text) for text in texts]
        gensim.corpora.MmCorpus.serialize('../Source/tmp/deerwester.mm',corpus)
        return corpus