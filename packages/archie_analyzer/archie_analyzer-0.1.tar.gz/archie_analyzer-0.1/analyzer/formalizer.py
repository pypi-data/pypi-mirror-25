import pandas as pd
import re

import requests

pairs={}   

LABEL = pd.read_csv('./data/classList.txt', header=None)
STOP = pd.read_csv('./data/stopwordList.txt', header=None) 

def readFormalizerFile():
    print("Reading lines...")
    lines = open('data/formalizerList.txt', encoding='utf-8').read().strip().split('\n')
    # Split every line into pairs and normalize
    # pairs = [[normalizeString(s) for s in l.split(" - ")] for l in lines]
    for l in lines:
        tempWords=[]
        for s in l.split(" - "):
            tempWords.append(s)
        pairs[tempWords[0]]=tempWords[1]
    
    print("total formalized words: %s, %s" % (len(pairs), len(lines)))
        
def formalizeSentence(sentence):
    rawSentence = normalizeString(sentence)
    # rawSentence = sentence
    newWords=[]
    for word in rawSentence.split(' '):
        if word in pairs:
            newWords.append(pairs[word])
        else:
            newWords.append(word)
    formalizedSentence = ' '.join(newWords)
    return formalizedSentence

def normalizeString(s):
    s = re.sub('[^a-zA-Z0-9 \n\.]', ' ', s)
    s = re.sub('\.\.+', ' ', s) 
    s = re.sub(r'[^\w]', ' ', s)
    s = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", s)
    s = re.sub(' +',' ',s)
    return s
