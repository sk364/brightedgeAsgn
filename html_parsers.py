# -*- coding: utf-8 -*-
"""
HTML parser classes
"""

import abc
import urllib2
import re
import sys

from bs4 import BeautifulSoup

from natural_language_processors import NaturalLanguageProcessor
from config import RATIO, INVALID_TAGS


class BaseHtmlParser(object):
	__metaclass__ = abc.ABCMeta


	@abc.abstractmethod
	def get_title_content(self):
		"""Gets title content found in <title> tag"""
		raise NotImplementedError


	@abc.abstractmethod
	def get_keywords_content(self):
		"""Gets content found in <meta name="keywords" ...> tag"""
		raise NotImplementedError


	@abc.abstractmethod
	def get_htags_content(self, hrange=0):
		"""Gets content in heading tags ('<h1>', '<h3>', etc.)
		:param: hrange: describes till which header tag to go to.
		example - hrange=4 will go till <h4>"""
		raise NotImplementedError


	@abc.abstractmethod
	def get_full_content(self):
		"""Gets full content of the webpage""" 
		raise NotImplementedError


class HtmlParser(BaseHtmlParser):
	"""
	Class to parse useful content in a given webpage.
	"""

	def __init__(self, url, nlp):
		"""
		Expects a `url` parameter to initialize the parser
		Raises `ValueError` if unable to get/parse content
		"""

		self.nlp = nlp
		self.soup = self._get_parser(url)
		self._replace_useless_tags()


	def get_title_content(self):
		"""
		Gets title content found in <title> tag

		:return: title content
		"""

		if not self.soup.title:
			return ''

		text = self._parse_node(self.soup.find('title'))
		return re.sub(r'\W+', ' ', text)


	def get_keywords_content(self):
		"""
		Gets content found in <meta name="keywords" ...> tag

		:return: keywords content
		"""

		meta_tag = self.soup.find("meta", {"name" : "keywords"})

		if not meta_tag:
			return ''

		return self.nlp.parse_text(meta_tag['content'])

 
	def get_htags_content(self, hrange=4):
		"""
		Gets content in heading tags ('<h1>', '<h3>', etc.)
		:param: hrange: describes till which header tag to go to.
		example - hrange=4 will go till <h4>

		:return: header tags content
		"""

		h_tags_content = []

		for i in xrange(hrange):
			h_tag = self.soup.find("h"+str(i))
			if h_tag:
				h_tags_content.append(self._parse_node(h_tag))

		return h_tags_content


	def get_full_content(self):
		"""
		Gets full content of the webpage
		"""

		full_content = []
		self._get_full_content(None, full_content)

		if not full_content:
			return ''

		return self.nlp.parse_text(" ".join(full_content))


	def _get_full_content(self, node, full_content):
		"""
		Recursively builds the content in `full_content` list until the density between tag and text is satisfy.
		:param: node: represents a tag
				full_content: result list
		"""

		if not node:
			node = self.soup

		if not len(str(node)):
			return

		ratio = len(node.get_text())/float(len(str(node)))
		if ratio > RATIO:
			full_content.append(self._parse_node(node) + " ")
		else:
			for node_child in node.findChildren(recursive = False):
				self._get_full_content(node_child, full_content)


	def _get_html_content(self, url):
		"""
		Gets content from url

		:return: content
		"""

		url_opener = urllib2.build_opener()
		url_opener.addheaders = [('Accept-Charset', 'utf-8')]
		content = url_opener.open(url, timeout=5).read()

		return content


	def _get_parser(self, url):
		"""
		Builds BeautifulSoup html parser

		:return: BeautfilSoup `utf-8` encoded parser
		"""

		try:
			content = self._get_html_content(url)
		except urllib2.URLError:
			raise ValueError('Unable to get content from {url}'.format(url=url))

		try:
			soup = BeautifulSoup(content, 'html.parser')
		except:
			raise ValueError('Unable to parse the content.')

		soup.encode('utf-8')

		return soup


	def _replace_useless_tags(self):
		"""
		Replaces useless tags in soup content

		:return: parser with removed useless content
		"""

		for script in self.soup('script'):
			script.replaceWith(" ")
		for link in self.soup('link'):
			link.replaceWith(" ")
		for style in self.soup('style'):
			style.replaceWith(" ")

		for tag in INVALID_TAGS: 
			for match in self.soup.findAll(tag):
				match.replaceWithChildren()


	def _parse_node(self, node):
		"""
		Parses the node to get text in it

		:return: text in node
		"""
		return self.nlp.parse_text(node.get_text())
