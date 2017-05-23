# -*- coding: utf-8 -*-

import os
import fnmatch
import re
import jieba
import gensim
import logging
import configparser
import redis

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename='WordGeneration.log',
                    filemode='w')

sourcePath = os.getcwd()
stopWords = r'stopkey.txt'
wordBin = r'word.bin'
configProperty = r'configFile'

redis_port = 6379
redis_host = '223.3.65.233'
redis_authenticate = "kseredis"
redis_db = '1'


def read_config():
    """
    this will give a configure of the StopWord fileName、the DocumentPath、stopWord path
    :return: None
    """
    global sourcePath, wordBin, stopWords, configProperty, redis_port, redis_host, redis_authenticate, redis_db

    config = configparser.ConfigParser()
    try:
        if os.path.exists(os.path.join(os.getcwd(),configProperty)):
            myfile = (os.path.join(os.getcwd(),configProperty))
            config.read(myfile)
            sourcePath = config.get('source', 'sourcePath')
            wordBin = config.get('config', 'wordBin')
            stopWords = config.get('source', 'stopWords')
            redis_host = config.get("config", "redis_host")
            redis_port = config.get("config", "redis_port")
            redis_authenticate = config.get("config", "redis_authenticate")
            redis_db = config.get("config", "redis_db")
    except IOError:
        logging.error("can't find the configFile")


def iter_find_files(path, fnexp):
    """
    find all the file of the current path
    :param path: the path to find the document
    :param fnexp: the regular expression used to filter the file
    :return: the list of document
    """
    allfile = []
    for root, dirs, files in os.walk(path):
        for filename in fnmatch.filter(files, fnexp):
            allfile.append(root + "\\" + filename)
    return allfile


def get_document():
    """
    find all the document of the file
    :return: document List
    """
    all_the_text = []
    documentcount = 0
    allhtmlFile = iter_find_files(sourcePath, "第*.html")
    logging.info('document_file_name_List: ')
    for fileName in allhtmlFile:
        logging.info(fileName.encode('gb2312'))
    for fileName in allhtmlFile:
        documentcount += 1
        file_object = open(fileName, 'r', encoding='utf-8')
        try:
            all_the_text.append(file_object.read())
        finally:
            file_object.close()
    logging.info("document number:" + str(documentcount))
    return all_the_text


def remove_tag(htmltag):
    """
    leaf the html tag
    :param htmltag:
    :return:
    """
    pattern = '<p.*?>.*?</p>'
    compiledPattern = re.compile(pattern)
    # print(sentence)
    result = compiledPattern.findall(htmltag)
    result = []
    # 去除标注的部分
    for part in result:
        senten, num = re.subn('<.*?>', '', part)
        result.append(senten)
    return result


def get_divide_word(alllist):
    """
    put the Sentence into Array
    :param alllist:  sentence List
    :return: sentence Array
    """

    resultList = []
    # result为章节和句子的二维数组
    for sentence in alllist:
        usefulList = remove_tag(sentence)
        resultList.append(usefulList)
    Allsentence = []
    for chapter in resultList:
        for paragrapher in chapter:
            sentence = re.split('。', paragrapher)
            for eachSentence in sentence:
                seg_list = jieba.cut(eachSentence, cut_all=False)
                Allsentence.append([" ".join(seg_list)])
    return Allsentence


def remove_stop_words(sentences):
    """
    :param sentences: arrayList
    :return: 去除停用词的词序列
    """
    stopKeys = []
    for root, dirs, files in os.walk(sourcePath):
        for filename in fnmatch.filter(files, stopWords):
            stopKeys.append([line.strip() for line in open(root + "\\" + filename).readlines()])
    stopKeys = stopKeys[0]
    for sentence in sentences:
        splitsentence = sentence[0].split(' ')
        # print(splitsentence)
        for word in splitsentence:
            if word in stopKeys:
                splitsentence.remove(word)
        sentence[0] = " ".join(splitsentence)
    return sentences


def connect_redis():
    """
    connect to redis
    return: the handler
    """
    pool = None
    try:
        if(pool==None):
            pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=1,password=redis_authenticate)
    except Exception:
        logging("连接Redis失败!")

    re = redis.Redis(connection_pool=pool)
    return re


def save_word_to_redis(re, model):
    """
    save the word to the Redis
    :param :
    :param re: the redis connect handler
    :param model: the word representation
    :return: isFinished
    """
    for word in model.wv.index2word:
        for vector in model.wv[word]:
            re.rpush(word, vector)


# _main_#

def main():
    read_config()
    model = gensim.models.Word2Vec.load(wordBin)
    sentence_array = []
    if model == None:
        allList = get_document()
        sentences = get_divide_word(allList)
        sentence_array = remove_stop_words(sentences)
        for sentence in sentence_array:
            if sentence[0] in [' ', '']:
                sentence_array.remove(sentence)

        # 转化为分词结果
        segment = []
        for i in range(len(sentence_array) - 1):
            segment.append(sentence_array[i][0].split(' '))
        model = gensim.models.Word2Vec(segment, min_count=1)
        model.save(wordBin)
        model.similarity()
    re = connect_redis()
    save_word_to_redis(re,model)

if __name__ == '__main__':
    main()
