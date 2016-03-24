from Html import *
import re

# -- configurations
_stopword_file = 'res/stopword.txt'

def parseText(txt):
	txt = txt.encode('utf-8','ignore')
	txt = txt.lower()
	txt = re.sub(r'([^\s\w]|_|\n|\t|\r)+', ' ', txt)
	txt = re.sub(' +',' ',txt)
	return txt

def oneGram(txt):
	counts = {}
	txts = txt.split(" ");
	for t in txts:
		if( t in counts ):
			counts[t]+=1
		else:
			counts[t]=1
	
	bag = []
	for c in counts:
		bag.append((c,counts[c]))
	return bag

def getStopword():
	words=[]
	with open(_stopword_file) as f:
		for line in f.readlines():
			words.append(line.strip('\n'))
	return words

def removeStopword(bag):
	stopwords = getStopword()
	newbag = []
	for b in bag:
		if(b[0] not in stopwords):
			newbag.append(b)
	return newbag

def sortBag(bag):
	bag = sorted(bag, key=lambda b: b[1])
	return bag

def mergeBag(bag1,bag2,weight=1):
	counts = {}
	for b in bag1: 
		counts[b[0]] = b[1]*weight
	for b in bag2: 
		if(b[0] in counts): 
			counts[b[0]]+=b[1]
		else:
			counts[b[0]]=b[1]
	# print counts
	ans = []
	for k in counts:
		ans.append((k,counts[k]))
	return ans

# for testing purpose
if __name__ == "__main__":
	# h = Html('http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster')
	# h = Html('http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/')
	h = Html('http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/')
	
	title = h.getTitle()
	keyword = h.getKeyword()
	hx = h.getHx()
	
	content = h.getContent()
	bag = oneGram(content)
	bag = removeStopword(bag)
	bag = sortBag(bag)
	bag = bag[-10:]
	print bag
