from itertools import chain
import numpy
import pickle
import re

CONVERGENCE_LIMIT = 0.00000001

# Load the link information
with open("links.dict",'rb') as f:
	links = pickle.load(f)

# Remove redundant links (i.e. same link in the document)
for l in links:
	links[l] = list(set(links[l]))


# One click step in the "random surfer model"
def surfStep(origin, links):
	dest = [0.0] * len(origin)
	for idx, proba in enumerate(origin):
		if len(links[idx])>0:
			w = 1.0 / len(links[idx])
		else:
			w = 0.0
		for link in links[idx]:
			dest[link] += proba*w
	return dest
#Filter the pages containing DNA and build a new source vector
#If you want to use this, take care of initializing the source vector with zeros before calling this function
def init_source_vector_with(pattern):

	r = re.compile(".*%s.*"%pattern)
	dna_pages = list(filter(r.match,allPages))
	for dna_page in dna_pages:
		sourceVector[allPages.index(dna_page)] = 1.0/len(dna_pages)



allPages = list(set().union(chain(*links.values()), links.keys()))
linksIdx = [ [allPages.index(target) for target in links.get(source,list())] for source in allPages ]



sourceVector = [1.0/len(allPages)] * len(allPages)

#sourceVector = [0.0/len(allPages)] * len(allPages)
#init_source_vector_with("DNA")

print(sum(sourceVector))
pageRanks = [1.0/len(allPages)] * len(allPages)
delta = float("inf")
#delta = 1000000
# Main loop for computing the Page Rank vector
k=1
while delta > CONVERGENCE_LIMIT:
	print("Total number of passes:",k)
	print("Convergence delta:", delta)
	pageRanksNew = surfStep(pageRanks, linksIdx)
	jumpProba = sum(pageRanks) - sum(pageRanksNew)
	if jumpProba < 0:  # Technical artifact due to numerical float approximation
		jumpProba = 0
	# Add some source vector to avoid the CHANGE_ME effect
	pageRanksNew = [ pageRank + jumpProba*jump for pageRank,jump in zip(pageRanksNew,sourceVector) ]
	delta = sum(numpy.abs(pageRanks[i] - pageRanksNew[i]) for i in range(len(pageRanks)))
	print("Convergence delta after pass n° {0} : {1} ".format(k, delta))
	pageRanks = pageRanksNew
	k += 1

# For information, what are the 10 highest ranked pages:
bestPages = reversed([ allPages[i] for i in numpy.argsort(pageRanks)[-10:] ])
bestPageRanks = reversed([ pageRanks[i] for i in numpy.argsort(pageRanks)[-10:] ])
for page,rank in zip(bestPages,bestPageRanks):
	print(page, "(rank score =", rank, ")")


# Name the entries of the pageRank vector
pageRankDict = dict()
for idx,pageName in enumerate(allPages):
	pageRankDict[pageName] = pageRanks[idx]

# Save the ranks as pickle object
with open("pageRank.dict",'wb') as fileout:
	pickle.dump(pageRankDict, fileout, protocol=pickle.HIGHEST_PROTOCOL)

# Page rank of the document "Charles Darwin"
# print("Charles Darwin","(rank score =",pageRankDict["Charles Darwin"],")")

