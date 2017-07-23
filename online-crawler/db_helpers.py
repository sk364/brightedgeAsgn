# -*- coding: utf-8 -*-
"""
Database helpers
"""

import sqlite3


def create_db_table(engine='sqlite3', db_name='db.sqlite3', table_name='example_table'):
    """Create table in db"""

    try:
        if engine == 'sqlite3':
            connection = sqlite3.connect(db_name)
            cursor = connection.cursor()

            create_query = "create table if not exists {table_name} (id integer primary key \
                            autoincrement, url text, title text, headings text, keywords text, \
                            full_content text);".format(table_name=table_name)

            cursor.execute(create_query)

            connection.commit()
            connection.close()
    except:
        return False

    return True


def store_in_db(engine='sqlite3', db_name='db.sqlite3', table_name='example_table', url=None, data=None):
    """
    Stores the data in specified db engine
    """

    if not (data and url):
        return False

    try:
        db_data = [url, data['title_content'], data['headings_content'], data['keywords_content'], data['full_content']]

        if engine == 'sqlite3':
            insert_query = "insert into {table_name} (url, title, headings, keywords, \
                            full_content) values (?, ?, ?, ?, ?);".format(table_name=table_name)

            connection = sqlite3.connect(db_name)
            cursor = connection.cursor()

            cursor.execute(insert_query, db_data)

            connection.commit()
            connection.close()
    except:
        return False

    return True


def fetch_from_db(engine='sqlite3', db_name='db.sqlite3', table_name='example_table', url=None):
    """Fetches data from db of the specified url"""

    if not url:
        return None

    try:
        if engine == 'sqlite3':
            select_query = "SELECT * from {table_name} where url=?".format(table_name=table_name)
            connection = sqlite3.connect(db_name)
            cursor = connection.cursor()

            cursor.execute(select_query, [url])
            db_data = cursor.fetchone()
    except:
        return None

    return db_data
