# -*- coding: utf-8 -*-
"""
Script to get html from the url and parse html to get relevant data
"""

import urllib2
from bs4 import BeautifulSoup
from tidylib import tidy_document


def get_html_content(url):
    """
    Gets content from url

    :return: content
    """

    url_opener = urllib2.build_opener()
    url_opener.addheaders = [('Accept-Charset', 'utf-8')]
    content = url_opener.open(url, timeout=5).read()

    return content


def get_parser(url):
    """
    Builds BeautifulSoup html parser

    :return: BeautfilSoup `utf-8` encoded parser
    """

    try:
        content = get_html_content(url)
    except urllib2.URLError:
        raise ValueError('Unable to get content from {url}'.format(url=url))

    try:
        soup = BeautifulSoup(content, 'html.parser')
    except:
        raise ValueError('Unable to parse the content.')

    soup.encode('utf-8')

    return soup


def crawl(url):
    """Crawls the url using custom HtmlParser instance"""

    try:
        parser = get_parser(url)

        title_content = [title.contents for title in parser.find_all('title')]
        keywords_content = [keyword.get('content', '') for keyword in parser.find_all('meta', {'name': 'keywords'})]
        htags_content = [
            {
                'h'+str(i): [content.contents[0] for content in parser.find_all('h'+str(i))]
            } for i in xrange(1,7)
        ]
        full_content = [tidy_document(str(content))[0] for content in parser.contents]
    except ValueError as err:
        return { 'success': False, 'message': str(err) }


    return {
        'success': True,
        'title_content': title_content,
        'keywords_content': keywords_content,
        'headings_content': htags_content,
        'full_content': full_content
    }


if __name__ == '__main__':
    print "Usage: Please run `python parse_app_api.py` to start the server\n"
