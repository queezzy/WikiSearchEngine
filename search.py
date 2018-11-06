from itertools import chain
import numpy
import pickle
import sys
import copy

with open("tokdoc.dict",'rb') as f:
	tokdoc = pickle.load(f)

with open("pageRank.dict",'rb') as f:
	pageRankDict = pickle.load(f)



Ntokens = sum(map(len,tokdoc.values()))
docList = list(set(chain(*tokdoc.values())))
Ndocs = len(docList)


tokInfo = dict()
tf = dict()
tfidf = dict()
# Compute the token information and count the token occurrences
for tok in tokdoc:
	tokInfo[tok] = -numpy.log(CHANGE_ME/Ndocs)
	for doc in tokdoc[tok]:
		if not doc in tf:
			tf[doc] = dict()
		tf[doc][tok] = tf[doc].get(tok,0) + 1

# Normalize token occurrences to token frequencies
for doc in tf:
	Ntok = sum(tf[doc].values())
	for tok in tf[doc]:
		tf[doc][tok] /= CHANGE_ME

# Compute the TF-IDF
for tok in tokdoc:
	for doc in tokdoc[tok]:
		if not doc in tfidf:
			tfidf[doc] = dict()
		tfidf[doc][tok] = CHANGE_ME

# Scalar product
def scal(query,doc,tfidf):
	s = float()
	for tok in query:
		s += tfidf[doc].get(tok,0)*tokInfo[tok]
	return s


# Ranked by token relevance (vector model)
def getBestResults(queryStr, topN):
	query = queryStr.split(" ")
	searchRes = list(map(lambda d:scal(query,d,tfidf),docList))
	bestPages = list(reversed([ docList[i] for i in numpy.argsort(searchRes)[-topN:] ]))
	return bestPages

# Page ranking of results
def rankResults(results):
	ranks = [ pageRankDict.get(page,0) for page in results ]
	rankedResults = list(reversed([ results[i] for i in numpy.argsort(ranks) ]))
	return rankedResults


def printResults(rankedResults):
	for idx,page in enumerate(rankedResults):
		print(str(idx) + ". " + page)



query = "evolution of bacteria"
top = 15
results = getBestResults(query,top)
printResults(results)
rankedResults = rankResults(results)
printResults(rankedResults)



