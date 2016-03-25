Word Density Analysis

Author : Kanit Srisuthep

Documentation :

https://docs.google.com/document/d/1Bh3WyRuA8ADDMbjGpyck1twVT4lmK06d22SypkwpcZk/edit
or pdf file in this folder WordDensityAnalysis.pdf

How to Execute :
	python main.py [url]
	python main.py http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/
	
	Some more test case here, please see top 3 lines.
	sh test.py

	
Example : 

http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/ref=sr_1_1?s=kitchen&ie=UTF8&qid=1431620315&sr=1-1&keywords=toaster
keywords : toaster, cuisinart, bread, slice, toast, 

http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/
keywords : friend, outdoors, introduce, indoorsy, keep, 

http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/
keywords : nsa, man, safeguard, leaks, liberty,


Descriptions :
	This program can extract keywords from any website. It takes url as an input, and produce 5 or less keyword as the output. The approach that I used is as follow:
		1. Download the given webpage
		2. Extract each part of the webpage using beautifulsoup library
			- Title
			- Meta keywords
			- Header
			- Content, for content we recursively search deep down in HTML tree and check the words vs tag density. i.e. <strong><u><i>w</strong></u></i> will have less word density than <i>words</i> (1/32 : 5/12)
		3. Normalize the word
			- make every words lowercase.
			- remove non-alphanumeric character, except space bar. e.g. !,@,#,$,\r,\t,\n
		4. Translate each of 4 part above to Bag of Word representation.
		5. Remove stopwords
		6. Merge all the bag, gives 3 times more weight to words from title,header, meta keywords
		7. Report the maximum word counting.

Architecture :
	There are 3 major parts : 
		Html Module : Responsible for web crawling.
		NLP Module : Responsible for word countings, and analysis. 
		Main Program : Responsible for taking input and perform program execution.

For coding detail please look at : 
	https://docs.google.com/document/d/1Bh3WyRuA8ADDMbjGpyck1twVT4lmK06d22SypkwpcZk/edit

Future Improvement
	1. Stemming and lemmatization, to make the words more matchable, ie. car and cars, manage and managing.
	2. From beautifulsoup library, When it extract the word from html subtree. It does not care about the meaning and spacebar. For example, <p>cat</p><p>dog</p>, it translates to catdog, which we know that it is in the different paragraph, so the text should be cat dog. In this case, there can effect the counting of the word that is near the beginning and the end of each tag. 
	3. For correctness, we might translate abbreviations to it full form. i.e. You'll = you will. This is just for correctness of algorithm but have not much impact since, from my observations, most of this cases happen with You'll I'll he's we're case, most of them are in stopwords list and will be removed eventually.
	4. We might try to use other topic model to capture the keyword from a text files, however we might need more dataset. For examples, LDA algorithm, it can automatically assign category for each webpage.
