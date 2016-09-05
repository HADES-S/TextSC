#!/usr/bin/python
#encoding=utf-8
#Script Name :LDA.py
#Author : Simon Shi
#created : 2016.8.30
#Version : 1.0
#Description : 对语料库中的数据进行主题模型处理

import os
from gensim import *
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
project_path = os.getcwd()
project_path = project_path[:project_path.find("TextSC")+6]

class LDA(object):
    dictionary = None
    corpus = None
    tfidf_corpus =None
    doc = None
    def __init__(self):
        if(os.path.exists(project_path+'\\Source\\tmp\\deerwester.dict')):
            self.dictionary = corpora.Dictionary.load(project_path+'\\Source\\tmp\\deerwester.dict')
            self.corpus = corpora.MmCorpus(project_path+'\\Source\\tmp\\deerwester.mm')
            self.TF()
            print("used files generated from first tutorial")
        else:
            print "something is wrong at the data set"
    def TF(self):
        #获取语料库的tf-idf向量
        tfidf = models.TfidfModel(corpus=self.corpus)
        self.tfidf_corpus=tfidf[self.corpus]
    def CLSI(self):
        lsi = models.LsiModel(self.tfidf_corpus,id2word=self.dictionary,num_topics=200)

        ver_bow = self.dictionary.doc2bow(self.doc)
        tfModel  =  models.TfidfModel(corpus=self.corpus)
        ver_bow = tfModel[ver_bow]
        ver_lsi = lsi[ver_bow]

        index = similarities.MatrixSimilarity(lsi[self.corpus])

        sims = index[ver_lsi]

        sims = sorted(enumerate(sims), key=lambda item: -item[1])#相似度高低排序
        print "LSI的结果输出"
        return sims[:10]

    def CLDA(self):

        lda = models.LdaModel(corpus= self.tfidf_corpus,id2word=self.dictionary,num_topics=200,update_every=0,passes=20)

        doc_bow = self.dictionary.doc2bow(self.doc)

        doc_lda = lda[doc_bow]

        index = similarities.MatrixSimilarity(lda[self.corpus])

        sims = index[doc_lda]

        sims = sorted(enumerate(sims),key=lambda item:-item[1])

        print "LDA的结果输出"
        return sims[:10]




