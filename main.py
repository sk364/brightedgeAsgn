from Html import *
from Nlp import *
import sys

# --- configurations 
# url = 'http://www.hello.com'
# url = 'http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster'
# url = 'http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/'
# url = 'http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/'
# url = 'http://www.theverge.com/2016/3/24/11291380/roku-tcl-tvs-availability-price'
# url = 'http://fathomaway.com/postcards/quirk/best-travel-blogs-and-websites/'
# url = 'http://www.geeksforgeeks.org/top-10-algorithms-in-interview-questions/'
# url = 'http://www-bcf.usc.edu/~feisha/'
# url = 'http://usc-actlab.github.io/'
# url = 'https://www.youtube.com/watch?v=px9iHkA0nOI&feature=youtu.be'
# url = 'http://abcnews.go.com/Politics/donald-trump-targets-ted-cruzs-wife-twitter/story?id=37889421'
# url = 'http://abcnews.go.com/Technology/wireStory/man-predicted-space-shuttle-challenger-disaster-dies-37881707'
# url = 'http://www.dailynews.com/government-and-politics/20160323/bernie-sanders-draws-big-crowd-at-las-wiltern-theater'
# url = 'http://www.amazon.com/gp/product/B00XGUXPVW/ref=s9_simh_gw_g79_i2_r?ie=UTF8&fpl=fresh&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=desktop-3&pf_rd_r=153M9PX3TW6EFWYM3XVM&pf_rd_t=36701&pf_rd_p=2437869462&pf_rd_i=desktop'
url = 'https://vimeo.com/56438232'
# -- todo 
# stemming
# remove stop words
# consecutive words i.e. this is a cat<strong>!</strong> shall be translated to this is a ***cat !***
# we may translate you'll to you will
# ycombinator ? 


# --- inputs 
sys.argv

# --- coding 
try:
	h = Html(url)	
except ValueError as e :
	print e
	sys.exit()

title = h.getTitle()
keyword = h.getKeyword()
hx = h.getHx()

content = h.getContent()
content = oneGram(content)
content = removeStopword(content)
content = sortBag(content)
content = content[-5:]

totalword = title + " " + keyword
for h in hx: totalword += " "+h
totalword = oneGram(totalword)
totalword = removeStopword(totalword)
totalword = sortBag(totalword)
totalword = totalword[-5:]

finalize = mergeBag(totalword,content,3)
finalize = sortBag(finalize)
finalize = list(finalize[-5:])

# print finalize
print 'keywords : ',
for w in finalize:
	print w[0],
print ''
