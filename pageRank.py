from itertools import chain
import numpy
import pickle

with open("links.dict",'rb') as f:
	links = pickle.load(f)


for l in links:
	links[l] = list(set(links[l]))



def surfStep(origin, links):
	dest = [0.0] * len(origin)
	for idx, proba in enumerate(origin):
		if len(links[idx]):
			w = 1.0 / len(links[idx])
		else:
			w = 0.0
		for link in links[idx]:
			dest[link] += proba*w
	return dest




allPages = list(set().union(chain(*links.values()), links.keys()))
linksIdx = [ [allPages.index(target) for target in links.get(source,list())] for source in allPages ]


pageRanks = [1.0/len(allPages)] * len(allPages)
sourceVector = [1.0/len(allPages)] * len(allPages)
delta = float("inf")

while delta > 0.0000001:
	print("Convergence delta:",delta,sum(pageRanks),len(pageRanks))
	pageRanksNew = surfStep(pageRanks, linksIdx)
	jumpProba = sum(pageRanks) - sum(pageRanksNew)
	if jumpProba < 0:
		jumpProba = 0
	pageRanksNew = [ pageRank + jump for pageRank,jump in zip(pageRanksNew,(p*jumpProba for p in sourceVector)) ]
	delta = sum([abs(p - pnew) for p,pnew in zip(pageRanks,pageRanksNew)])
	pageRanks = pageRanksNew

bestPages = [ allPages[i] for i in numpy.argsort(pageRanks)[-10:] ]
bestPageRanks = [ pageRanks[i] for i in numpy.argsort(pageRanks)[-10:] ]

pageRankDict = dict()
for idx,pageName in enumerate(allPages):
	pageRankDict[pageName] = pageRanks[idx]




# Save the ranks as pickle object
with open("pageRank.dict",'wb') as fileout:
	pickle.dump(pageRankDict, fileout, protocol=pickle.HIGHEST_PROTOCOL)

