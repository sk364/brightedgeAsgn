# -*- coding: utf-8 -*-
"""
Script to test the Word Density Analyzer
"""

import argparse
import sys
from word_density_analyzers import WordDensityAnalyzer

# set the recursion limit to 50,000
sys.setrecursionlimit(50000)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--url', required=True, help='URL of a webpage.')
    parser.add_argument('-t', '--topics', required=False, type=int, help='Number of topics in the result.')

    return vars(parser.parse_args())


args = parse_args()
url = args['url']
topic_count = args.get('topics', 5)    # using default topic count as 5

wda = WordDensityAnalyzer(url, topic_count=topic_count, stopwords_file='resources/stopwords.txt')

# parse the data and get the content from the webpage
parsed_data = wda.parse_data()

title = parsed_data['title']
keywords = parsed_data['keywords']
hx_tags_content = parsed_data['hx_tags_content']
full_content = parsed_data['full_content']

all_words = "{title} {keywords}".format(title=title, keywords=parsed_data['keywords'])
for hx_content in hx_tags_content:
    all_words += " " + hx_content

# Prepare the word bags of miscellaneous and full content
prepared_words_bag = wda.prepare_bag(all_words)
prepared_full_content_bag = wda.prepare_bag(full_content)


# get the most relevant topics from the bags
most_relevant_topics = wda.get_most_relevant_topics(
    prepared_words_bag,
    prepared_full_content_bag,
    misc_words_weight=3
)

# print the output consisting of the webpage url and the topics of it
print "Webpage : {url}".format(url=url)

if not most_relevant_topics:
    print 'No topics found!'
else:
    print 'Most Relevant Topics : ',
    print ", ".join([topic[0] for topic in most_relevant_topics])

print
