#!/usr/bin/python
#encoding=utf-8
#Script Name :LDA.py
#Author : Simon Shi
#created : 2016.8.30
#Version : 1.0
#Description : 对语料库中的数据进行主题模型处理

import os
from gensim import *
import MyCorpora,logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class LDA(object):
    dictionary = None
    corpus = None
    tfidf_corpus =None
    def __init__(self):
        if(os.path.exists('..//Source//tmp//deerwester.dict')):
            self.dictionary = corpora.Dictionary.load('..//Source//tmp//deerwester.dict')
            self.corpus = corpora.MmCorpus('/tmp/deerwester.mm')
            print("used files generated from first tutorial")
        else:
            print "something is wrong at the data set"
    def TF(self):
        #获取语料库的tf-idf向量
        tfidf = models.TfidfModel(corpus=self.corpus)
        self.tfidf_corpus=tfidf[self.corpus]
    def LSI(self):
        lsi = models.LsiModel(self.tfidf_corpus,id2word=self.dictionary,num_topics=200)

        ver_bow = self.dictionary.doc2bow(self.doc)
        ver_lsi = lsi[ver_bow]

        index = similarities.MatrixSimilarity(lsi[self.corpus])

        sims = index[ver_lsi]

        sims = sorted(enumerate(sims), key=lambda item: -item[1])#相似度高低排序

        print sims[:10]

    def LDA(self):

        lda = models.LdaModel(cropus = self.tfidf_corpus,id2word=self.dictionary,num_topics=200,update_every=0,passes=20)

        doc_bow = self.dictionary.doc2bow(self.doc)
        doc_lda = lda[doc_bow]
        index = similarities.MatrixSimilarity(lda[self.corpus])

        sims = index[doc_lda]

        sims = sorted(enumerate(sims),key=lambda item:-item[1])

        print sims[:10]




