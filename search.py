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
for tok in tokdoc:
	tokInfo[tok] = -numpy.log(len(set(tokdoc[tok]))/Ndocs)
	for doc in tokdoc[tok]:
		if not doc in tf:
			tf[doc] = dict()
		tf[doc][tok] = tf[doc].get(tok,0) + 1

for doc in tf:
	Ntok = sum(tf[doc].values())
	for tok in tf[doc]:
		tf[doc][tok] /= Ntok


for tok in tokdoc:
	for doc in tokdoc[tok]:
		if not doc in tfidf:
			tfidf[doc] = dict()
		tfidf[doc][tok] = tf[doc].get(tok,0)*tokInfo[tok]


tfidfNorm = copy.deepcopy(tfidf)
for doc in tfidf:
	norm = numpy.sqrt(sum([val*val for val in tfidf[doc].values()]))
	for tok in tfidf[doc]:
		tfidfNorm[doc][tok] = tfidf[doc][tok]/norm

def scal(query,doc,tfidf):
	s = float()
	for tok in query:
		s += tfidf[doc].get(tok,0)*tokInfo[tok]
	return s

def scalNorm(query,doc,tfidf):
	s = float()
	for tok in query:
		s += tfidfNorm[doc].get(tok,0)*tokInfo[tok]
	return s

# Ranked by token relevance (vector model)
def getBestResultsNormed(queryStr, topN):
	query = queryStr.split(" ")
	searchRes = list(map(lambda d:scalNorm(query,d,tfidf),docList))
	bestPages = list(reversed([ docList[i] for i in numpy.argsort(searchRes)[-topN:] ]))
	return bestPages


# Ranked by token relevance (vector model)
def getBestResults(queryStr, topN):
	query = queryStr.split(" ")
	searchRes = list(map(lambda d:scal(query,d,tfidf),docList))
	bestPages = list(reversed([ docList[i] for i in numpy.argsort(searchRes)[-topN:] ]))
	return bestPages

def rankResults(results):
	ranks = [ pageRankDict.get(page,0) for page in results ]
	rankedResults = list(reversed([ results[i] for i in numpy.argsort(ranks) ]))
	return rankedResults


def printResults(rankedResults):
	for idx,page in enumerate(rankedResults):
		print(str(idx) + ". " + page)


#queryStr = sys.argv[1]
query = "evolution of bacteria"
top = 15
results = getBestResults(query,top)
printResults(results)


results = getBestResultsNormed(query,top)
printResults(results)

rankedResults = rankResults(results)
printResults(rankedResults)

#bestPageSimilarity = list(reversed([ searchRes[i] for i in numpy.argsort(searchRes)[-10:] ]))
#bestPageSimilarity


