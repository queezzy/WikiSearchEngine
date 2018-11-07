from itertools import chain
import numpy
import pickle

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
		if len(links[idx]):
			w = 1.0 / CHANGE_ME
		else:
			w = 0.0
		for link in links[idx]:
			dest[link] += proba*w
	return dest




allPages = list(set().union(chain(*links.values()), links.keys()))
linksIdx = [ [allPages.index(target) for target in links.get(source,list())] for source in allPages ]


sourceVector = [1.0/len(allPages)] * len(allPages)
pageRanks = [1.0/len(allPages)] * len(allPages)
delta = float("inf")

# Main loop for computing the Page Rank vector
while delta > CONVERGENCE_LIMIT:
	print("Convergence delta:",delta)
	pageRanksNew = surfStep(pageRanks, linksIdx)
	jumpProba = sum(pageRanks) - sum(pageRanksNew)
	if jumpProba < 0: # Technical artifact due to numerical float approximation
		jumpProba = 0
	# Add some source vector to avoid the CHANGE_ME effect
	pageRanksNew = [ pageRank + jumpProba*jump for pageRank,jump in zip(pageRanksNew,sourceVector) ]
	delta = CHANGE_ME
	pageRanks = pageRanksNew

# For information, what are the 10 highest ranked pages:
bestPages = reversed([ allPages[i] for i in numpy.argsort(pageRanks)[-10:] ])
bestPageRanks = reversed([ pageRanks[i] for i in numpy.argsort(pageRanks)[-10:] ])
for page,rank in zip(bestPages,bestPageRanks):
	print(page,"(rank score =",rank,")")


# Name the entries of the pageRank vector
pageRankDict = dict()
for idx,pageName in enumerate(allPages):
	pageRankDict[pageName] = pageRanks[idx]




# Save the ranks as pickle object
with open("pageRank.dict",'wb') as fileout:
	pickle.dump(pageRankDict, fileout, protocol=pickle.HIGHEST_PROTOCOL)

