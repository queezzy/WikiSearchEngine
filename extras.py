sourceVector = [1 if "DNA" in a else 0 for a in pageRankDict.keys()]
sourceVector = [s/sum(sourceVector) for s in sourceVector]
pageRanks = [1.0/len(allPages)] * len(allPages)
delta = float("inf")


tau = 0.8
CONVERGENCE_LIMIT = 0.00000001


while delta > CONVERGENCE_LIMIT:
	print("Convergence delta:",delta,sum(pageRanks),len(pageRanks))
	pageRanksNew = surfStep(pageRanks, linksIdx)
	jumpProba = sum(pageRanks) - sum(pageRanksNew)
	if jumpProba < 0: # Technical artifact due to numerical errors
		jumpProba = 0
	pageRanksNew = [ tau*pageRank + (1-tau)*jump for pageRank,jump in zip(pageRanksNew,sourceVector) ]
	delta = sum([abs(p - pnew) for p,pnew in zip(pageRanks,pageRanksNew)])/len(pageRanks)
	pageRanks = pageRanksNew

bestPages = [ allPages[i] for i in numpy.argsort(pageRanks)[-20:] ]
bestPages


# Name the entries of the pageRank vector
pageRankDict = dict()
for idx,pageName in enumerate(allPages):
	pageRankDict[pageName] = pageRanks[idx]

pageRankDict["DNA"] > pageRankDict["RNA"]

