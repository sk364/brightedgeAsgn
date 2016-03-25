import urllib2
import re
from bs4 import BeautifulSoup
from Nlp import *
import bs4
import sys
sys.setrecursionlimit(50000)

#----- configurations
_ratio = 0.75

class Html:
	
	def __init__(self,url):
		try:
			opener = urllib2.build_opener()
			opener.addheaders = [('Accept-Charset', 'utf-8')]
			content = opener.open(url, timeout=5).read()
		except:
			raise ValueError('Unable to get content from '+url)
		
		try:
			soup = BeautifulSoup(content)
			soup.encode('utf-8')
			[s.replaceWith(" ") for s in soup('script')]
		except:
			raise ValueError('Unable to parse the content')
		[s.replaceWith(" ") for s in soup('link')]
		[s.replaceWith(" ") for s in soup('style')]

		invalid_tags = ['b', 'i', 'u', 'strong', 'a']
		for tag in invalid_tags: 
			for match in soup.findAll(tag):
				match.replaceWithChildren()

		self.soup = soup;
		pass;

	def parseNode(self,node):
		# for r in node:
		# 	print r.encode('utf-8','ignore')
		# 	if (r.string is None):
		# 		r.string = ' '
		return parseText(node.get_text())

	def getTitle(self):
		if(self.soup.title == None):
			return "";
		else:
			txt = self.parseNode(self.soup.find('title'))
			return re.sub(r'\W+', ' ', txt)

	def getKeyword(self):
		tag = self.soup.find("meta", {"name":"keywords"})
		if(tag== None):
			return "";
		else:
			return parseText(tag['content']);

	def getHx(self):
		ans = []

		tag = self.soup.find("h1")
		if(tag != None):
			ans.append(self.parseNode(tag))

		tag = self.soup.find("h2")
		if(tag != None):
			ans.append(self.parseNode(tag))

		tag = self.soup.find("h3")
		if(tag != None):
			ans.append(self.parseNode(tag))

		tag = self.soup.find("h4")
		if(tag != None):
			ans.append(self.parseNode(tag))


		return ans;

	def getContent(self):
		ans=[]
		str = ""
		self.getContentRes(None,ans)
		for txt in ans: 
			str+= txt+" "
		return parseText(str)

	def getContentRes(self,node,ans):
		if(node == None):
			node = self.soup
		
		if(len(str(node)) == 0):
			return
		ratio = len(node.get_text())/float(len(str(node)))
		if(ratio > _ratio):
			# print "\n\n\n\n\n\n\n--"
			# print self.parseNode(node)+" "
			# print ratio
			# print "\n\n\n\n\n\n\n--"
			ans.append(self.parseNode(node)+" ")
		else:
			for i in range(len(node.findChildren(recursive = False))):
				self.getContentRes(node.findChildren(recursive = False)[i],ans)
	

# for testing purpose
if __name__ == "__main__":
	# h = Html('http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster')
	# h = Html('http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/')
	h = Html('http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/')
	
	print "title:\t",h.getTitle()
	print "keyword:\t",h.getKeyword()
	print "hx:\t",h.getHx()
	print "content:\t"
	print h.getContent()


