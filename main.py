# coding=utf-8
from Html import Html 
import sys

# --- configurations 
url = 'http://www.hello.com'


# --- coding 
try:
	html = Html(url)	
except ValueError as e :
	print e
	sys.exit()

print html.getTitle()
# print soup.find("meta", {"name":"keywords"})
