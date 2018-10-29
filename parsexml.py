import sys
import xml.etree.ElementTree
import re
import pickle
import glob
from itertools import chain

xmlFiles = list(chain(*[ glob.glob(globName)  for globName in sys.argv[1:] ]))
print("Files as input:", xmlFiles)

docs = dict()


print("Parsing XML...")
for xmlFile in xmlFiles:
	pages = xml.etree.ElementTree.parse(xmlFile).getroot()

	for page in pages.findall("{http://www.mediawiki.org/xml/export-0.10/}page"):
		titles = page.findall("{http://www.mediawiki.org/xml/export-0.10/}title")
		revisions = page.findall("{http://www.mediawiki.org/xml/export-0.10/}revision")
	
		if titles and revisions:
			revision = revisions[0] # last revision
			contents = revision.findall("{http://www.mediawiki.org/xml/export-0.10/}text")
			if contents:
				docs[titles[0].text] = contents[0].text 



# Some regEx
linkRe = "\[\[([^\]]+)\]\]"
removeLinkRe = "\[\[[^\]]+\|([^\|\]]+)\]\]"
removeLink2Re =  "\[\[([^\|\]]+)\]\]"
wordRe = "[a-zA-Z\-]+"
stopWords = ["-"]


print("Extracting links, transforming links in text, tokenizing, ans filling a tok-doc matrix...")
links = dict()
tokdoc = dict()
for idx,doc in enumerate(docs):
	if idx%(len(docs)/20) == 0:
		print("Progress " + str(idx*100/len(docs))  +"%")
	for link in re.finditer(linkRe,docs[doc]):
		target = link.group(1).split('|')[0]
		if target in docs.keys():
			#print(doc + " --> " + target)
			links[doc] = links.get(doc,list()) + [target]
			

	# transform links to text
	docs[doc] = re.sub(removeLinkRe,r"\1",docs[doc])
	docs[doc] = re.sub(removeLink2Re,r"\1",docs[doc])
	
	for wordre in re.finditer(wordRe,docs[doc]):
		word = wordre.group(0).lower()
		if word not in stopWords:
			tokdoc[word] = tokdoc.get(word,list()) + [doc]

for word in tokdoc:
	tokdoc[word].sort()

print("Saving the links and the tokdoc as pickle objects...")
with open("links.dict",'wb') as fileout:
	pickle.dump(links, fileout, protocol=pickle.HIGHEST_PROTOCOL)

with open("tokdoc.dict",'wb') as fileout:
	pickle.dump(tokdoc, fileout, protocol=pickle.HIGHEST_PROTOCOL)

