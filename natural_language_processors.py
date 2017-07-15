# -*- coding: utf-8 -*-
"""
Natural Language Processor classes
"""

import abc
import re


class BaseNaturalLanguageProcessor(object):
	"""
	Base class for natural language processing
	"""

	__metaclass__ = abc.ABCMeta


	@abc.abstractmethod
	def parse_text(self, text):
		"""Parses the text to return text without redundant symbols"""
		raise NotImplementedError


	@abc.abstractmethod
	def get_words_count(self, text):
		"""Prepares a bag of words with their corresponding counts"""
		raise NotImplementedError


	@abc.abstractmethod
	def remove_stopwords(self, bag):
		"""Removes stopwords from the bag of words"""
		raise NotImplementedError


	@abc.abstractmethod
	def sort_bag(self, bag):
		"""Sorts the bag corresponding to its count"""
		raise NotImplementedError


	@abc.abstractmethod
	def merge_bag(self, bag1, bag2, bag1_weight=1, bag2_weight=1):
		"""Merges two bags with word counts calculated based on bag weights"""
		raise NotImplementedError


class NaturalLanguageProcessor(BaseNaturalLanguageProcessor):
	"""
	Class to process text and get useful content in it
	"""

	def __init__(self, stopwords_file=''):
		"""
		Initializes the class with `stopwords_file` path
		Wrong file path will set `stopwords` to an empty list.
		"""

		self.stopwords = self._get_stopwords(stopwords_file)


	def parse_text(self, text):
		"""
		:param: text: Text to parse
		:return: Processed text with removed tabs, spaces, new lines, plus signs
		"""

		if not text:
			return ''

		lowered_text = text.encode('utf-8','ignore').lower()
		stripped_text = re.sub(r'([^\s\w]|_|\n|\t|\r)+', ' ', lowered_text)
		stripped_text = re.sub(' +', ' ', stripped_text)
		
		return stripped_text


	def get_words_count(self, text):
		"""
		:param: text: Text to get words count from
		:return: bag of words. Format -> [('words1',1),('words2',2),('words3',3)]
		"""

		if not text:
			return []

		word_counts = {}
		words = text.split(" ")

		for word in words:
			if not (word in word_counts):
				word_counts[word] = 0
			
			word_counts[word] += 1

		bag = [(c, word_counts[c]) for c in word_counts]
		return bag


	def remove_stopwords(self, bag):
		"""
		Removes stopwords from the bag of words
		:param: bag: Bag of words
		:return: Bag with removed stopwords
		"""

		if not bag:
			return []

		removed_stopwords_bag = [word_info for word_info in bag if word_info[0] not in self.stopwords]
		return removed_stopwords_bag


	def sort_bag(self, bag):
		"""
		Sorts bag according to more frequency of word
		:param: bag: Bag of words
		:return: Sorted bag
		"""

		if not bag:
			return []

		return sorted(bag, key=lambda b: b[1])


	def merge_bag(self, bag1, bag2, bag1_weight=1, bag2_weight=1):
		"""
		Merges two bags with word counts dependent on bag weights
		:param: bag1: first bag of words
				bag2: second bag of words
				bag1_weight: Weight of bag1
				bag2_weight: Weight of bag2

		:return: Merged bag
		"""

		if not bag1:
			bag1 = []

		if not bag2:
			bag2 = []

		bag_counts = {}

		for word_info in bag1:
			bag_counts[word_info[0]] = word_info[1] * bag1_weight

		for word_info in bag2:
			if not (word_info[0] in bag_counts):
				bag_counts[word_info[0]] = 0
			bag_counts[word_info[0]] += word_info[1] * bag2_weight

		return [(k, bag_counts[k]) for k in bag_counts]


	def _get_stopwords(self, stopwords_file):
		"""
		Returns the content of the `stopwords_file`
		:param: stopwords_file: File path to stopwords_file
		:return: stopwords file content, if path file is correct, else empty list
		"""

		try:
			with open(stopwords_file) as f:
				return [line.strip('\n') for line in f.readlines()]
		except IOError:
			pass

		return []	# if file path is incorrect
