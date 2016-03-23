# coding=utf-8
from httpreq import Http 
import sys

# --- configurations 
url = 'http://www.cnn.com'


# --- coding 

http = Http()

try:
	soup = http.getContent(url)
except ValueError as e :
	print e
	sys.exit()

print soup.title
print soup.find("meta", {"name":"keywords"})