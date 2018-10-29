
import json
import httplib2
import urllib
from urllib.parse import urlencode, quote_plus

categoryToCrawl = "Category:Biology"
crawlingDepth = 4


def getPages(category):
	h = httplib2.Http()
	params = dict()
	params["cmlimit"] = "500"
	params["list"] = "categorymembers"
	params["action"] = "query"
	params["format"] = "json"
	params["cmtitle"] = category
	encodedParams = urlencode(params)
	(resp_headers, content) = h.request("http://en.wikipedia.org/w/api.php?" + encodedParams, "GET")
	jsonContent = content.decode('utf-8')
	j = json.loads(jsonContent)["query"]["categorymembers"]
	return j

j = getPages(categoryToCrawl)
realPages = list()
for depth in range(crawlingDepth):
	toGet = list()
	for k in j:
		page = k["title"]
		if page.startswith("Category:"):
			toGet+=getPages(page)
		realPages += [k["title"]]
		print(k["title"])
	j = toGet

