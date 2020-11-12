from itertools import chain
import numpy
import pickle
import math
import copy

with open("tokdoc.dict", 'rb') as f:
	tokdoc = pickle.load(f)

with open("pageRank.dict", 'rb') as f:
	pageRankDict = pickle.load(f)



Ntokens = sum(map(len, tokdoc.values()))
docList = list(set(chain(*tokdoc.values())))
Ndocs = len(docList)


tokInfo = dict()
tf = dict()
tfidf = dict()
# Compute the token information and count the token occurrences
for tok in tokdoc:
	tokInfo[tok] = -numpy.log(len(list(set(tokdoc[tok])))/Ndocs)
	for doc in tokdoc[tok]:
		if not doc in tf:
			tf[doc] = dict()
		tf[doc][tok] = tf[doc].get(tok,0) + 1

# Normalize token occurrences to token frequencies
for doc in tf:
	Ntok = sum(tf[doc].values())
	for tok in tf[doc]:
		tf[doc][tok] /= Ntok

# Compute the TF-IDF
for tok in tokdoc:
	for doc in tokdoc[tok]:
		if not doc in tfidf:
			tfidf[doc] = dict()
		tfidf[doc][tok] = tf[doc].get(tok,0)*tokInfo[tok]
		if(tfidf[doc][tok]<0.0):
			print(tfidf[doc][tok])

# Save tokInfo to be used in the latent semantic script
with open("tokinfo.dict",'wb') as fileout:
			pickle.dump(tokInfo, fileout, protocol=pickle.HIGHEST_PROTOCOL)

# Save the TF-IDF as pickle object
def save_tfidf(normalize=True):

	if normalize:
		
		tfidf_normalize = dict()
		
		for doc in tfidf:

			if not doc in tfidf_normalize:
				tfidf_normalize[doc] = dict()
			
			norm = math.sqrt(sum(map(lambda t: t**2,tfidf[doc].values())))
			
			for tok in tfidf[doc]:
				tfidf_normalize[doc][tok] = tfidf[doc][tok]/norm
		
		with open("TF-IDF.dict",'wb') as fileout:
			pickle.dump(tfidf_normalize, fileout, protocol=pickle.HIGHEST_PROTOCOL)
	
	else:
		with open("TF-IDF.dict",'wb') as fileout:
			pickle.dump(tfidf, fileout, protocol=pickle.HIGHEST_PROTOCOL)

save_tfidf()

# Scalar product
def scal(query,doc,tfidf,normalize=False):
	s = float()
	query_vector_norm_2 = 0.0
	doc_vector_norm_2 = 0.0
	for tok in query:
		s += ((tfidf[doc].get(tok,0))*tokInfo.get(tok,0))
		query_vector_norm_2 += tokInfo.get(tok,0) ** 2
	
	if normalize and query_vector_norm_2>0:
		for t in tfidf[doc].values():
			doc_vector_norm_2 += t ** 2
		return s/(math.sqrt(query_vector_norm_2)*math.sqrt(doc_vector_norm_2))
	else:
		return s


# Ranked by token relevance (vector model)
def getBestResults(queryStr, topN,normalize=False):
	query = queryStr.lower().split(" ")
	searchRes = list(map(lambda d: scal(query, d, tfidf,normalize), docList))
	bestPages = list(reversed([docList[i] for i in numpy.argsort(searchRes)[-topN:] ]))

	return bestPages,list(reversed(numpy.sort(searchRes)[-topN:]))

# Page ranking of results
def rankResults(results):
	ranks = [pageRankDict.get(page, 0) for page in results]
	rankedResults = list(reversed([results[i] for i in numpy.argsort(ranks) ]))
	return rankedResults


def printResults(rankedResults,scal_score=None):
	for idx, page in enumerate(rankedResults):
		score = 0.0
		if scal_score is not None:
			score = scal_score[idx]
		print("%d. %s . Score: %f . PageRank: %f"%(idx,page,score,pageRankDict.get(page,0)))



query = "RNA"
top = 15

print("\nTOP %d RESULTS FOR QUERY: \"%s\" "%(top,query))
results,scores = getBestResults(query, top,False)
print("\n---- RESULTS WITHOUT NORMALIZING TFIDF AND QUERY VECTORS ----")
print("\n		--------- TOP RESULTS WITH PAGE RANKED BY TOKEN RELEVANCE ---------")
printResults(results,scores)

results,scores = getBestResults(query, top,False)
print("\n--------- TOP RESULTS WITH PAGE RANKED BY PAGE AUTHORITY ---------")
rankedResults = rankResults(results)
printResults(rankedResults,scores)

results,scores = getBestResults(query, top,True)
print("\n---- RESULTS WITH NORMALIZING TFIDF AND QUERY VECTORS ----")
print("\n		--------- TOP RESULTS WITH PAGE RANKED BY TOKEN RELEVANCE ---------")
printResults(results,scores)

results,scores = getBestResults(query, top,True)
print("\n--------- TOP RESULTS WITH PAGE RANKED BY PAGE AUTHORITY ---------")
rankedResults = rankResults(results)
printResults(rankedResults,scores)

print("Page Rank of %s : %f"%(query,pageRankDict.get(query,0)))