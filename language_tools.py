class LanguageHelper:
    """
    This is a class that determines if a word is in a set of words and suggests other words based on an imput.
    
    Attributes:
        words: An iterable sequence of strings that define the words in the language.
    """
    
    def __init__(self, words):
        """
        The constructor for LanguageHelper class.
        
        Parameters:
            words: An iterable sequence of strings that define the words in the language. 
        """
        self._wordSet = set()
        
        if hasattr(words, 'read'): # if words is a file it will convert the contents to a readable format
            languageFile = words.read()
            languageFile = languageFile.splitlines()
            
            for w in languageFile:
                self._wordSet.add(w.strip())
                
        else: # if words is anything else it will add the contents to a set 
            for w in words: 
                self._wordSet.add(w.strip())
            
    def __contains__(self, query):
        """
        Determines if given word is in set of words. 
        
        Parameters:
            query (str): A word that might be in the set of words.
        
        Returns: 
            bool: Returns True if the value is in the set of words. Returns False if the word is not in the set of words.
        """
        
        if query in self._wordSet: # Check to see if query is in the set of words
            return True
        if query.lower() in self._wordSet: # Checks to see if the lowercase version of query is in the set of words
            return True
        else:
            return False
        
    def getSuggestions(self, query):
        """
        Gives word suggestions from set of words that are one edit away from inputted word.
        
        Parameters:
            query (str): A word to get suggestions for
        
        Returns:
            list: Returns a list of suggested words that are one edit away from the input.
        """
    
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        suggestions = []
        
        # Switches out every letter in query with each letter from the alphabet and checks if its in the language.
        for a in list(alphabet):   
            for i in range(len(query)):
                changedLetter = list(query)
                if query[i].isupper():  # if the letter is a capital letter we want to replace it with another capital 
                    changedLetter[i] = a.upper()
                    changedLetter = ''.join(changedLetter)
                else:
                    changedLetter[i] = a
                    changedLetter = ''.join(changedLetter)
                if changedLetter in self._wordSet or changedLetter[0].lower() + changedLetter[1:] in self._wordSet:  # Put the new word into suggestions if it or its uncapitalized version is in language
                    suggestions.append(changedLetter)
                    
        
        # Removes a letter from the word one position at a time and determines if the new word is in the language.   
            if len(query) > 1: # Only runs if query has more than one letter 
                for i in range(len(query)):
                    removedLetter = query[:i] + query[i+1:]
                    if removedLetter in self._wordSet or removedLetter.lower() in self._wordSet:
                            suggestions.append(removedLetter)
                    
        # Adds each letter of the alphabet to the word one position at a time and determines if the new word is in the language.      
        for a in list(alphabet):
            for i in range(len(query)+1):
                addLetter = query[:i] + a + query[i:]
                if addLetter in self._wordSet:
                    suggestions.append(addLetter)
                if addLetter[0].isupper and addLetter[1:].islower() and addLetter.lower() in self._wordSet: # Only adds word if it requires to just add a letter, not add a letter and make it uppercase
                    suggestions.append(addLetter)
        
        # Inverts two neighboring letters at a time.
        # Checks to see if each new word is in the language and adds it to suggestions if it is.
        for i in range(len(query)-1):
            queryAsList = list(query)
            queryAsList[i], queryAsList[i+1] = queryAsList[i+1], queryAsList[i]
            invertedLetters = ''.join(queryAsList)
            if invertedLetters in self._wordSet or invertedLetters.lower() in self._wordSet:
                    suggestions.append(invertedLetters)
        
        #If the given word is lowercase but the language contains a capital version of the word it gets added to the suggestion list           
        if query.capitalize() in self._wordSet:
            suggestions.append(query.capitalize())
        
        # Adds the word itself to the list if its in the langauge
        if query in self._wordSet:
            suggestions.append(query)
        
        # Capitalizes one letter in a word if the rest is uppercase and in language. Ex NaTO to NATO
        for i in range(len(query)):
            if query[i].islower:
                newWord =list(query)
                newWord[i] = query[i].upper()
                newWord = ''.join(newWord)
                if newWord in self._wordSet:
                    suggestions.append(newWord)
            
        # Changes the word to lowercase if the lowercase word exists ex. cUt to cut or CUt to Cut
        if query[0].isupper() and query.lower() in self._wordSet:
            suggestions.append(query.capitalize())
        if query[0].islower() and query.lower() in self._wordSet:
            suggestions.append(query.lower())
        
        # Removing duplicates from suggestion list
        finalSuggestions = []
        for s in suggestions:
            if s not in finalSuggestions:
                finalSuggestions.append(s)
                
        return sorted(finalSuggestions)
