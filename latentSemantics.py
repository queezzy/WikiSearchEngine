import pickle
import scipy.sparse as sp
from scipy.sparse.linalg import svds
import matplotlib.pyplot as plt
from collections import Counter
from itertools import chain
import numpy

with open("TF-IDF.dict", 'rb') as f:
	tfidf = pickle.load(f)

with open("tokinfo.dict", 'rb') as f:
	tokinfo = pickle.load(f)

with open("pageRank.dict", 'rb') as f:
	pageRankDict = pickle.load(f)

allPages = list(tfidf.keys())
map_tok_idx = dict()

def build_sparse_matrix_from_tfidf_inverted_index():
    rows, cols, vals = [], [], []

    current_max_col_idx = 0
    for idx,doc in enumerate(allPages):
        for tok in tfidf[doc]:
            if tok in map_tok_idx:
                cols.append(map_tok_idx.get(tok))
            else:
                map_tok_idx[tok]=current_max_col_idx
                cols.append(current_max_col_idx)
                current_max_col_idx+=1
            rows.append(idx)
            vals.append(tfidf[doc][tok])

    return sp.csr_matrix((vals,(rows,cols)))

M = build_sparse_matrix_from_tfidf_inverted_index()

#The value of 200 has been chosen after having plot a set of 1000 first singular values and
#we used the elbow method to cut at 200

u, s, vt = svds(M,k=200,which='LM',return_singular_vectors=True)

#fig,ax = plt.subplots()
#ax.plot(list(range(len(lambdas))),list(reversed(lambdas)),label="Singular values")
#ax.set_ylabel("singular value")
#ax.set_title("Singluar value plot")
#ax.legend()
#plt.show()


# We want to project elements from M_toProject on the concept space M_concept
#Those parameters should be on sparse format csr
def project_documents_on_concepts_space(M_concept, M_toProject):
	
    return M_concept.dot(M_toProject)

K = project_documents_on_concepts_space(sp.csc_matrix(vt),M.transpose())
print(K.shape)

def scal(query):
	
    rows,cols,vals = [],[],[]

    query_counter = Counter(query)
    for tok in query_counter.keys() :
        
        if tok in map_tok_idx:
            
            rows.append(0)
            cols.append(map_tok_idx[tok])
            vals.append((query_counter.get(tok)*tokinfo.get(tok,0))/sum(query_counter.values()))
    query_projected = project_documents_on_concepts_space(sp.csc_matrix(vt),sp.csr_matrix((vals,(rows,cols)),shape=(1,M.shape[1])).transpose())

    return K.transpose().dot(query_projected)


# Ranked by token relevance (vector model)
def getBestResults(queryStr, topN):
	query = queryStr.lower().split(" ")
	searchRes = list(chain(*scal(query).toarray()))
	bestPages = list(reversed([allPages[i] for i in numpy.argsort(searchRes)[-topN:] ]))

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

query = "evolution of bacteria"
top = 15

print("\nTOP %d RESULTS FOR QUERY: \"%s\" "%(top,query))
results,scores = getBestResults(query, top)
print("\n---- RESULTS WITH SVD OVER TFIDF ----")
print("\n		--------- TOP RESULTS WITH PAGE RANKED BY TOKEN RELEVANCE ---------")
printResults(results,scores)

results,scores = getBestResults(query, top)
print("\n--------- TOP RESULTS WITH PAGE RANKED BY PAGE AUTHORITY ---------")
rankedResults = rankResults(results)
printResults(rankedResults,scores)