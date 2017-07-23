# -*- coding: utf-8 -*-
"""
Flask server api to crawl websites
"""

from flask import Flask, request, jsonify
from parse import crawl

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    """
    Endpoint to get data from the url

    ---

    parameters:
        - name: url
        - type: string
        - description: URL to crawl html from
        - required: true

    responseMessages:
        - status: 200
        - message: JSON data containing parsed content

        - status: 400
        - message: 
    """

    data = request.form

    url = data.get('url', '')
    if url:
        resp = crawl(url)
        return jsonify(resp)
    else:
        resp, code = {'success': 'false', 'message': 'Required Field: URL missing'}, 400
        return jsonify(resp), code


if __name__ == '__main__':
    app.run()