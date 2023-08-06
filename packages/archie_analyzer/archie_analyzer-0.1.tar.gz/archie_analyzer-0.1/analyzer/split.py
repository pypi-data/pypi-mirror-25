from textblob import TextBlob
import pandas as pd

LABEL = pd.read_csv('./data/classList.txt', header=None)
STOP = pd.read_csv('./data/stopwordList.txt', header=None)
REMOVE = pd.read_csv('./data/stopwordContains.txt', header=None)

def split_tokens(message):
    return TextBlob(str(message)).words

def split_lemmas(message):
    words = TextBlob(str(message)).words
    return [word.lemma for word in words]

def split_stopwords(message):
    words = TextBlob(str(message)).words
    return [word.lemma for word in words if word not in set(STOP[0])]

def remove_words(message):
	removeList = REMOVE[0].tolist()
	removed=[]
	words = TextBlob(str(message)).words
	for word in words:
		for rem in removeList:
			if rem in word and word not in removed:
				removed.append(word)
	return ' '.join([word.lemma for word in words if word not in removed])
