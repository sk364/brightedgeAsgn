# -*- coding: utf-8 -*-
"""
Flask server api to crawl websites
"""

from flask import Flask, request, jsonify
from parse import crawl
from db_helpers import create_db_table, store_in_db

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
        is_created = create_db_table(db_name='crawler.sqlite3', table_name='website_data')
        is_stored = store_in_db(db_name='crawler.sqlite3', table_name='website_data', url=url, data=data)

        resp = crawl(url)

        if is_created and is_stored:
            resp['db_message'] = 'Successfully stored in database.'
        else:
            resp['db_message'] = 'Couldn\'t store in database.'

        return jsonify(resp)
    else:
        resp, code = { 'success': 'false', 'message': 'Required Field: URL missing' }, 400
        return jsonify(resp), code


if __name__ == '__main__':
    app.run()