import os
from nltk import word_tokenize
import itertools
import pandas as pd
import openpyxl
import math
import numpy as np

#below exists so pandas doesnt freak out when I run the professors code
pd.options.mode.chained_assignment = None  # default='warn'

#amount of documents in the corpus
number_of_documents = 106

# setting up windows file formatting
if os.name == 'nt':    #check if windows 
  a='\\'

#get all the file names within the inFile
files = os.listdir(
    r'C:\Users\dhain\Desktop\Web&Text\Hw3\output')


tokenizedList = []

for file in files:

    #open the file with encoding
    filePath = "C:" + a + "Users" + a + "dhain" + a + "Desktop" + a + "Web&Text" + a + "Hw3" +a + "output" +  a + file

    with open(filePath, encoding="latin-1") as f: 
        cleaned_article = f.readlines()

    cleaned_article = cleaned_article[0]
    
    tokenizedList.append(word_tokenize(cleaned_article))

#combine all the seperate lists into one single list
combinedTokenizedList = list(itertools.chain.from_iterable(tokenizedList))

#create the vocabulary
vocabulary = sorted(set(combinedTokenizedList))


#create empty data frame with columns being the file names & rows being the vocab
tfidf_vectors = pd.DataFrame(index=vocabulary, columns=files)

#how many times each token appears in the respective article
i = 0
for doc in tokenizedList:
    for token in tfidf_vectors.index:
        tfidf_vectors[tfidf_vectors.columns[i]].loc[token] = doc.count(token)
    i = i+1

#number of articles each token appears in
tfidf_vectors['corpus_term_freq'] = tfidf_vectors.gt(0).sum(axis=1) 

#set up idf column with nan as the values for all rows
tfidf_vectors['idf'] = np.nan

#calvulate idf value
for token in tfidf_vectors.index:
    idf = round((math.log(number_of_documents/tfidf_vectors['corpus_term_freq'].loc[token]))**2,5)
    tfidf_vectors['idf'].loc[token] = idf


# creating the tf-idf values for all words in the vocab.
# multiply the term frequency by the idf 
for file in files:
    name = file + "_tfidf"
    tfidf_vectors[name] = tfidf_vectors['idf']*tfidf_vectors[file]

#removing all the extraneous columns
for file in files:
    tfidf_vectors = tfidf_vectors.drop(file, axis=1)
tfidf_vectors = tfidf_vectors.drop('corpus_term_freq', axis = 1)
tfidf_vectors = tfidf_vectors.drop('idf', axis = 1)

tfidf_vectors.to_excel("group_1_tfidf_vectors.xlsx")
print("done")

