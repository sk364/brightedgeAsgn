import urllib2
from bs4 import BeautifulSoup

class Http:
	def __init__(self):
		pass;

	def getContent(self,url):
		try:
			content = urllib2.urlopen(url, timeout=5).read()
		except:
			raise ValueError('Unable to get content from '+url)

		try:
			soup = BeautifulSoup(content)
			soup.encode('utf-8')
		except:
			raise ValueError('Unable to parse the content')
			
		return soup
