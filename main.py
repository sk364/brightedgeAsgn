from Html import *
from Nlp import *
import sys
import pydoc 

# -- document 
# https://docs.google.com/document/d/1Bh3WyRuA8ADDMbjGpyck1twVT4lmK06d22SypkwpcZk/edit

# -- todo 
# stemming
# consecutive words i.e. this is a cat<strong>!</strong> shall be translated to this is a ***cat !***
# we may translate you'll to you will
# ycombinator ?

# --- command line check
if(len(sys.argv) == 1 ): 
	print 'Usage : python main.py [url]'
	sys.exit()

# --- collecting data
try:
	h = Html(sys.argv[1])
except ValueError as e :
	print e
	sys.exit()

# --- parsing data
title = h.getTitle()
keyword = h.getKeyword()
hx = h.getHx()

# --- simple bag of word on content
content = h.getContent()
content = oneGram(content)
content = removeStopword(content)
content = sortBag(content)
content = content[-5:]

# --- simple bag of word on title, meta keywords, h1-h4
totalword = title + " " + keyword
for h in hx: totalword += " "+h
totalword = oneGram(totalword)
totalword = removeStopword(totalword)
totalword = sortBag(totalword)
totalword = totalword[-5:]

# --- merge bag, give weight more to title/meta/h1-h4 than content.
finalize = mergeBag(totalword,content,3)
finalize = sortBag(finalize)
finalize = list(finalize[-5:])
finalize.reverse()

# --- print finalize
print "Webpage : "+sys.argv[1]
print 'Keywords :',
for w in finalize:
	print w[0]+",",
print ''

