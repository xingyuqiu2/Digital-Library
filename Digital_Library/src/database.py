"""
This module is used to connect database and update or insert
books/authors into the database.
"""
import json
import os
import logging

from bson.json_util import dumps
import pymongo
from dotenv import load_dotenv

BOOK_ATTRIBUTES = {'book_url', 'title', 'book_id', 'ISBN', 'author_url', 'author', 'rating',
                   'rating_count', 'review_count', 'image_url', 'similar_books'}
AUTHOR_ATTRIBUTES = {'name', 'author_url', 'author_id', 'rating', 'rating_count',
                     'review_count', 'image_url', 'related_authors', 'author_books'}


def remove_empty_string(my_dict):
    """
    Remove keys with empty string in dict
    """
    list_keys = []
    for key in my_dict.keys():
        if isinstance(my_dict[key], str) and my_dict[key] == '':
            list_keys.append(key)
    for key in list_keys:
        my_dict.pop(key)
    return my_dict


class Database:
    """
    Database class that stores the database and tables using mongoDB
    """

    def __init__(self):
        """
        Connect to database and initialize books/authors tables
        """
        load_dotenv()
        self.client = pymongo.MongoClient(os.getenv('HOST'), os.getenv('PORT'))
        self.digital_library_db = self.client['Digital_Library']
        self.books_tb = self.digital_library_db.books_table
        self.authors_tb = self.digital_library_db.authors_table

    def is_book_exist(self, book_dic):
        """
        Check whether book exists in books table
        """
        book_id = book_dic['book_id']
        book_info = self.books_tb.find_one({'book_id': book_id})
        if book_info:
            return True
        return False

    def is_author_exist(self, author_dic):
        """
        Check whether author exists in authors table
        """
        author_id = author_dic['author_id']
        author_info = self.authors_tb.find_one({'author_id': author_id})
        if author_info:
            return True
        return False

    def update_insert_from_json_file(self, json_file):
        """
        Update on or insert into the existing books/authors tables from json file.
        Handle invalid json file and malformed data structure.
        """
        with open(json_file, 'r') as file:
            try:
                content = json.load(file)
            except ValueError:
                logging.error('Invalid JSON file: File given is not a valid JSON file')
                return
        if not isinstance(content, dict):
            print('Malformed data structure: Content of JSON file is not a dict')
            return
        array_books = content['books']
        array_authors = content['authors']
        for book_dic in array_books:
            book_dic = remove_empty_string(book_dic)
            if 'book_id' not in book_dic.keys():
                # Skip if no book_id
                print('Skip one book from json file with no id')
                continue
            if self.is_book_exist(book_dic):
                # book already exist in database, update valid attributes
                self.update_books_tb_from_json(book_dic)
            else:
                # book not exist in database, insert valid attributes
                self.insert_books_tb_from_json(book_dic)
        for author_dic in array_authors:
            author_dic = remove_empty_string(author_dic)
            if 'author_id' not in author_dic.keys():
                # Skip if no author_id
                print('Skip one author from json file with no id')
                continue
            if self.is_author_exist(author_dic):
                # Author already exist in database, update valid attributes
                self.update_authors_tb_from_json(author_dic)
            else:
                # Author not exist in database, insert valid attributes
                self.insert_authors_tb_from_json(author_dic)

    def update_books_tb_from_json(self, book_dic):
        """
        Update books table from JSON file.
        Only update value in valid attributes
        """
        book_dic = remove_empty_string(book_dic)
        book_id = book_dic['book_id']
        my_query = {'book_id': book_id}
        for attribute in book_dic.keys():
            if attribute not in BOOK_ATTRIBUTES:
                print(f'Malformed data structure: '
                      f'Book with id {book_id} has invalid attribute {attribute}')
                continue
            new_values = {'$set': {attribute: book_dic[attribute]}}
            self.books_tb.update_one(my_query, new_values)
            print(f'{attribute} entry of book with id {book_id} is updated')

    def update_authors_tb_from_json(self, author_dic):
        """
        Update authors table from JSON file.
        Only update value in valid attributes
        """
        author_dic = remove_empty_string(author_dic)
        author_id = author_dic['author_id']
        my_query = {'author_id': author_id}
        for attribute in author_dic.keys():
            if attribute not in AUTHOR_ATTRIBUTES:
                print(f'Malformed data structure: '
                      f'Author with id {author_id} has invalid attribute {attribute}')
                continue
            new_values = {'$set': {attribute: author_dic[attribute]}}
            self.authors_tb.update_one(my_query, new_values)
            print(f'{attribute} entry of author with id {author_id} is updated')

    def insert_books_tb_from_json(self, book_dic):
        """
        Insert into books table from JSON file.
        Only insert valid attributes and skip invalid attributes
        """
        book_dic = remove_empty_string(book_dic)
        invalid_keys = []
        book_id = book_dic['book_id']
        for attribute in book_dic.keys():
            if attribute not in BOOK_ATTRIBUTES:
                print(f'Malformed data structure: '
                      f'Book with id {book_id} has invalid attribute {attribute}')
                invalid_keys.append(attribute)
        for key in invalid_keys:
            book_dic.pop(key, None)
        self.insert_books_tb(book_dic)
        print(f'Book with id {book_id} is created')

    def insert_authors_tb_from_json(self, author_dic):
        """
        Insert into authors table from JSON file.
        Only insert valid attributes and skip invalid attributes
        """
        author_dic = remove_empty_string(author_dic)
        invalid_keys = []
        author_id = author_dic['author_id']
        for attribute in author_dic.keys():
            if attribute not in AUTHOR_ATTRIBUTES:
                print(f'Malformed data structure: '
                      f'Author with id {author_id} has invalid attribute {attribute}')
                invalid_keys.append(attribute)
        for key in invalid_keys:
            author_dic.pop(key, None)
        self.insert_authors_tb(author_dic)
        print(f'Author with id {author_id} is created')

    def update_insert_books_tb(self, book_dic):
        """
        Update on or insert book_dic into books table in database
        If book title exists in table, then update.
        Otherwise, insert into table
        """
        book_dic = remove_empty_string(book_dic)
        book_id = book_dic['book_id']
        if self.is_book_exist(book_dic):
            # If book_id already exist in table, then update the book
            self.update_books_tb(book_dic, book_id)
            print(f'Book with id {book_id} is updated')
        else:
            # Book does not exist, then insert
            self.insert_books_tb(book_dic)
            print(f'Book with id {book_id} is created')

    def update_insert_authors_tb(self, author_dic):
        """
        Update on or insert author_dic into authors table in database
        If author name exists in table, then update.
        Otherwise, insert into table
        """
        author_dic = remove_empty_string(author_dic)
        author_id = author_dic['author_id']
        if self.is_author_exist(author_dic):
            # If author_id already exist in table, then update the author
            self.update_authors_tb(author_dic, author_id)
            print(f'Author with id {author_id} is updated')
        else:
            # Author does not exist, then insert
            self.insert_authors_tb(author_dic)
            print(f'Author with id {author_id} is created')

    def update_books_tb(self, book_dic, book_id):
        """
        Update book_dic in books table
        """
        self.books_tb.delete_one({'book_id': book_id})
        self.insert_books_tb(book_dic)

    def update_authors_tb(self, author_dic, author_id):
        """
        Update author_dic in authors table
        """
        self.authors_tb.delete_one({'author_id': author_id})
        self.insert_authors_tb(author_dic)

    def insert_books_tb(self, book_dic):
        """
        Insert book_dic into book table
        """
        self.books_tb.insert_one(book_dic)

    def insert_authors_tb(self, author_dic):
        """
        Insert author_dic into author table
        """
        self.authors_tb.insert_one(author_dic)

    def export_to_json_file(self):
        """
        Export existing books/authors into JSON files from database.
        JSON file name is 'library.json'
        """
        dictionary = {'books': [], 'authors': []}
        for book_info in self.books_tb.find({}, {'_id': 0}):
            book_info_dic = json.loads(dumps(book_info))
            dictionary['books'].append(book_info_dic)
        for author_info in self.authors_tb.find({}, {'_id': 0}):
            author_info_dic = json.loads(dumps(author_info))
            dictionary['authors'].append(author_info_dic)
        with open('src/library.json', 'w') as output_file:
            json.dump(dictionary, output_file, indent=4)
