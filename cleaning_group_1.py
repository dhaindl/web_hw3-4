import os
import string
import nltk
import re
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet
from nltk.corpus import stopwords



# setting up windows file formatting
if os.name == 'nt':    #check if windows 
  a='\\'

#get all the file names within the inFile
files = os.listdir(
    r'C:\Users\dhain\Desktop\Web&Text\Hw3\inFilesTest')

#get the output file path
outfile = "C:" + a+ "Users" + a + "dhain" + a +  "Desktop" + a + "Web&Text" + a + "Hw3" + a + "output" + a

for file in files:

    #open the file with encoding
    filePath = "C:" + a + "Users" + a + "dhain" + a + "Desktop" + a + "Web&Text" + a + "Hw3" +a + "inFilesTest" +  a + file
    
    #apparently latin-1 is the only enconding that will work for all 80 files
    with open(filePath, encoding="latin-1") as f: 
        example_article = f.readlines()

    #remove first three lines, they are the name of the article/date/etc
    example_article = example_article[3:]

    updated_example_article = []

    #remove new lines
    for i in range(len(example_article)):
        if example_article[i] != '\n':
            updated_example_article.append(example_article[i].replace('\n', ''))

    #lower case
    for i in range(len(updated_example_article)):
        updated_example_article[i] = updated_example_article[i].lower()

    #create a string of the article, remove contractions
    updated_example_article = ' '.join(updated_example_article)
    updated_example_article = updated_example_article.replace('\'s', '')


    #remove any links inside the article, ie: twitter/help
    updated_example_article = re.sub(r"\w+\/\w*\/?", "", updated_example_article)
    #remove numbers
    updated_example_article = re.sub(r'[0-9]+', '', updated_example_article)

    # tried to remove words that start with a certain character

    updated_example_article = re.sub(r'(\s)#\w+', r'\1', updated_example_article)
    updated_example_article = re.sub(r'(\s)\'\w+', r'\1', updated_example_article)
    updated_example_article = re.sub(r'(\s)\\\w+', r'\1', updated_example_article)
    updated_example_article = re.sub(r'(\s)^\w+', r'\1', updated_example_article)

    updated_example_article = re.sub(r'(\s)-\w+', r'\1', updated_example_article)



    # concatenate common adjectives
    updated_example_article = updated_example_article.replace('not ', 'not_')
    updated_example_article = updated_example_article.replace('never ', 'never_')
    updated_example_article = updated_example_article.replace('rarely ', 'rarely_')


    #remove commas and periods and other things
    updated_example_article = updated_example_article.replace(',', '')
    updated_example_article = updated_example_article.replace('.', '')
    updated_example_article = ''.join(
        [str(char) for char in updated_example_article if char in string.printable])


    #lemmatize
    text = word_tokenize(updated_example_article)


    tagged_article = pos_tag(text, tagset='universal')

    # Init the Wordnet Lemmatizer
    lemmatizer = WordNetLemmatizer()

    lemmatized_sentence = []
        
    for word in tagged_article:
        
        mapped_tag = ''
        
        if word[1] in ['ADJ', 'NOUN', 'VERB', 'ADV']:
            
            if word[1]=='NOUN':
    #             print('nn')
                mapped_tag=wordnet.NOUN
            if word[1]=='VERB':
    #             print('vv')
                mapped_tag=wordnet.VERB
            if word[1]=='ADJ':
    #             print('aa')
                mapped_tag=wordnet.ADJ
            if word[1]=='ADV':
    #             print('rr')
                mapped_tag=wordnet.ADV
                
            lemmatized_sentence.append(lemmatizer.lemmatize(word[0], mapped_tag))
        else:
            lemmatized_sentence.append(word[0])
            

    # assign a set of stopwords to a set called stops
    # added other punctuation to the list
    stops = list(stopwords.words('english'))
    stops = list(stopwords.words('english')) + ['10', '%', 'however', 'ever', '[', ']', ';', '?', '@', '*', ':'
                                                , '(', ')', '!', '|', 'llc', '`', '#', '$', '--', '`', '``',"''", "'",
                                                "url", "http", "-", "&", "/", "+", ">"] 

    article_no_stopwords = []

    # loop over all words in words
    for word in lemmatized_sentence:
        
        # check if each word is in stops, casefold() will ignore capitalization, 
        # note that all the stop words above are lowercase
        if word.casefold() not in stops:
            article_no_stopwords.append(word)
            

    newF = outfile + "cleaned_" + file 
    f2 = open(newF, "w")
    article_no_stopwords = ' '.join(article_no_stopwords)
    f2.write(article_no_stopwords)
    f.close()
    f2.close()
