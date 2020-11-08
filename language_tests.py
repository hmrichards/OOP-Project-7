from language_tools import LanguageHelper
import unittest

# We define the custom lexicon that we will use for our controlled tests
lexicon = ('car', 'cat', 'Cate', 'cater', 'care',
           'cot', 'cute', 'dare', 'date', 'dog', 'dodge',
           'coffee', 'pickle', 'grate')

class BasicTest(unittest.TestCase):

    def setUp(self):
        self.help = LanguageHelper(lexicon)
  
    # make sure that all the words in the lexicon are recognized
    def testContainment(self):
        for w in lexicon:
            self.assertTrue(w in self.help)
  
    def testFailures(self):
        self.assertFalse('cate' in self.help)     # only allowed when capitalized
        self.assertFalse('fox' in self.help)      # word is not there
        self.assertFalse('cofee' in self.help)    # mis-spell word is not there

    def testSuggestInsertion(self):
        self.assertEqual(self.help.getSuggestions('pikle'), ['pickle'])
        self.assertEqual(self.help.getSuggestions('ct'), ['cat','cot'])

    def testSuggestDeletion(self):
        self.assertEqual(self.help.getSuggestions('gratle'), ['grate'])

    def testSuggestionsCapitalization(self):
        self.assertEqual(self.help.getSuggestions('Gate'), ['Cate', 'Date', 'Grate'])

    def testSuggestionsNone(self):
        self.assertEqual(self.help.getSuggestions('blech'), [])


#------------More complicated tests------------- 

# New language for the tests
language = ('NATO', 'Rome', 'weird', 'wired', 'ball', 'balls')

class MyTests(unittest.TestCase):
    
    def setUp(self):
        self.test = LanguageHelper(language)
    
    def testContainsCapitalization(self):
        self.assertTrue(self.test.__contains__('Ball')) # Should be true since ball is in langauge
    
    def testQueryInSuggestions(self):
        self.assertEqual(self.test.getSuggestions('ball'), ['ball', 'balls']) # the query should be included in suggestions list
    
    def testInvertedCharacters(self):
        self.assertEqual(self.test.getSuggestions('wierd'), ['weird', 'wired'])
        
    def testSuggestionCapitalization(self):
        self.assertEqual(self.test.getSuggestions('NaTO'), ['NATO']) # should capitalize one letter to get word in language
        self.assertEqual(self.test.getSuggestions('rome'), ['Rome']) # should capitalize first letter to get proper noun in language
    
    
    
        

if __name__ == '__main__':
    unittest.main()
