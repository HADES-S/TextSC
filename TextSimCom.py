#!/usr/bin/python
# -*- coding:utf-8-*-
import logging
from extractComponent import extractTool
import Topic
class TextSimCom(object):
    if __name__=="__main__":
        mylda = Topic.LDA()
        mylda.doc = u""
        print "输入:"+str(mylda.doc.encode('utf-8'))
        corporas = Topic.MyCorpora("InputParameter.txt","stopWords.txt")
        mylda.doc = corporas.convertQuery(mylda.doc)
        documents = corporas.turnToList("InputParameter.txt")
        sim1 = mylda.CLSI()
        for num in sim1:
            print documents[num[0]]
        sim2 = mylda.CLDA()
        for num in sim2:
            print documents[num[0]]
