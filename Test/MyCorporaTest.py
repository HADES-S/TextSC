import unittest
import Topic


class MyTestCase(unittest.TestCase):
    crop =None
    def setUp(self):
        self.crop= Topic.MyCorpora("InputParameter.txt","stopWords.txt")

    def test_document(self):
        document = self.crop.turnToList("InputParameter.txt")
        #print(document)

    def test_words(self):
        stopwords = self.crop.useStopWords("stopWords.txt")
       # print(stopwords)

    def test_vector(self):
        self.crop.getVector()

if __name__ == '__main__':
    unittest.main()
