#!/usr/bin/python
#encoding=utf-8
#Script Name :extractedTool.py
#Author : Simon Shi
#created : 2016.08.28
#Version : 1.0
#Description : 抽取数据库中的规则文本，转换成参数和谓词
import commands,os,string,ConfigParser
import MySQLdb,re,logging,datetime,sys
class extractText(object):
    '连接数据库，输出数据库特定目录'
    host = '127.0.0.1'
    user = 'admin'
    password = 'admin'
    dbname = 'dbname'
    port = 3306
    charset = ''
    sql = "select input from TestRule"
    saveParameterPath = "InputParameter.txt"
    savePredicatePath = "InputPredicate.txt"
    dataBaseConfigPath = '/jdbc.config'
    conn = None
    cur = None
    def __init__(self):
        self.getConfig();
        self.loggingConfig()

    def connectDatabase(self):
        '''
        连接数据库，返回游标
        :return:
        '''
        try:
            print self.host,self.user,self.password,self.dbname,self.port
            self.conn=MySQLdb.connect(host=self.host,user=self.user,passwd=self.password,db=self.dbname,port=int(self.port),charset=self.charset)
            self.cur=self.conn.cursor()
            logging.info("database connected successfully")
            self.cur.execute(self.sql)
        except MySQLdb.Error,e:
            logging.error( "Mysql Error %d: %s" % (e.args[0], e.args[1]))
        return self.cur

    def closeDataBase(self):
        '''
        关闭与数据库的连接
        :return:
        '''
        try:
            self.cur.close()
            self.conn.close()
        except MySQLdb.Error,e:
            logging.error( "Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def convertText(self,text,ParameterObject,dict1):
        '''
        转换数据，存入预定义文本
        :param text: 文本
        :param ParameterObject: 文件类
        :param dict1: 映射，用来判断相似性
        :return:
        '''
        text = re.sub("\[.*?\]| |\.","",text) #非贪婪匹配去除所有的概率部分和空格
        text = re.sub("[^\(\),]*\(","",text)
        text = re.sub("\)","",text)
        part = text.split(',')
        for partNum in part:
            logging.info(partNum+" take in successfully")
            #添加hash防止重复
            if(partNum not in dict1 and partNum[0].isalpha()and partNum[0]>u'\u4e00' and partNum[0]<u'\u9FFF'):
                ParameterObject.write(partNum.encode('utf-8'))
                ParameterObject.write('\n')
                dict1[partNum] = 1

    def getConfig(self):
        config = ConfigParser.ConfigParser()
        path = os.path.abspath('config')+"\\"+ self.dataBaseConfigPath
        config.read(path)
        self.dbname = config.get("database","dbname")
        self.host = config.get("database","host")
        self.user = config.get("database","dbuser")
        self.password = config.get("database","dbpassword")
        self.port = config.get("database","port")
        self.charset = config.get("database","charset")

    def loggingConfig(self):
        Date = datetime.date.today()
        if(not os.path.exists(os.path.abspath('log')+'\\tmp')):
            os.makedirs(os.path.abspath('log')+'\\tmp')
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filename=os.path.abspath('log')+'\\tmp\\'+str(Date.year)+'_'+str(Date.month)+'_'+str(Date.day)+'.log',
                    filemode='a')

    def saveText(self):
        try:
            cur = self.connectDatabase()
            saveParameterPath = os.path.abspath("Source")+ "\\"+self.saveParameterPath
            savePredicatePath = os.path.split(os.path.realpath(__file__))[0]+ self.savePredicatePath
            ParameterObject = open(saveParameterPath,mode='a',buffering=-1)
            dict1 = {}
            for temp in cur._rows:
                resultSet=cur.fetchone()
                print resultSet[0]
                self.convertText(resultSet[0],ParameterObject,dict1)
            ParameterObject.close()
            self.closeDataBase()
        except MySQLdb.Error,e:
            logging.error( "Mysql Error %d: %s" % (e.args[0], e.args[1]))