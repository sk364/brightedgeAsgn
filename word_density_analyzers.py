# -*- coding: utf-8 -*-
"""
Word Density Analyzer classes
"""

import sys
from html_parsers import HtmlParser
from natural_language_processors import NaturalLanguageProcessor


class WordDensityAnalyzer:
    """
    Class for performing word density analysis
    """

    def __init__(self, url, topic_count=5, stopwords_file=''):
        """
        Initializes the HtmlParser and NaturalLanguageProcessor classes with
        count of topics the user wants in the result
        :param: url: URL of the webpage
                topic_count: Number of topics in the result
                stopwords_file: Stopwords file path
        """

        self.nlp = NaturalLanguageProcessor(stopwords_file=stopwords_file)

        try:
            self.html_parser = HtmlParser(url, self.nlp)
        except ValueError as e:
            print e
            sys.exit()

        self.topic_count = topic_count


    def parse_data(self):
        """
        Parses data using HtmlParser to get title, meta keywords, header tags
        content and the full content
        """

        return {
            'title': self.html_parser.get_title_content(),
            'keywords': self.html_parser.get_keywords_content(),
            'hx_tags_content': self.html_parser.get_htags_content(),
            'full_content': self.html_parser.get_full_content()
        }


    def prepare_bag(self, content):
        """
        Prepares word bag in which the words are mapped to their respective counts
        in the `content`
        """

        words_count_bag = self.nlp.get_words_count(content)
        removed_stopwords_bag = self.nlp.remove_stopwords(words_count_bag)
        sorted_bag = self.nlp.sort_bag(removed_stopwords_bag)
        prepared_bag = sorted_bag[-self.topic_count:]

        return prepared_bag


    def get_most_relevant_topics(self, misc_words, full_content, misc_words_weight=1, full_content_weight=1):
        """
        Gets the most relevant topics from two bag of words
        :param: misc_words: Different type of content from the page
                full_content: Full content of the page
                misc_words_weight: Weight of the `misc_words` bag
                full_content_weight: Weight of the `full_content` bag
        """

        merged_bag = self.nlp.merge_bag(
            misc_words,
            full_content,
            bag1_weight=misc_words_weight,
            bag2_weight=full_content_weight
        )

        sorted_bag = self.nlp.sort_bag(merged_bag)[-self.topic_count:]
        sorted_bag.reverse()

        return sorted_bag
