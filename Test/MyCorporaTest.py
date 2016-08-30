import unittest
import Topic.MyCorpora

class MyTestCase(unittest.TestCase):
    crop =None
    def setUp(self):
        self.crop= Topic.MyCorpora.MyCorpora()

    def test_document(self):
        document = self.crop.turnToList("InputParameter.txt")
        print(document)

    def test_words(self):
        stopwords = self.crop.useStopWords("stopWords.txt")
        print(stopwords)
if __name__ == '__main__':
    unittest.main()
