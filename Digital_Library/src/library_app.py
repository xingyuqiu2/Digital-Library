"""
Web api using flask which supports GET, PUT, POST, DELETE.
Error message and HTTP status code (200, 400, 415, 404) is returned if error occurs in web api.
Only error message is returned if functions in this file is used in other local files.
"""
import json

from flask import Flask, jsonify, request, make_response, render_template
from bson.json_util import dumps

from src.database import Database
from src.book_scraper import is_book, scrape_book_page
from src.author_scraper import is_author, scrape_author_page
from src.query import query, check_content_type, MALFORMED_QUERY_STRING, OBJECT_NOT_EXIST, \
    FIELD_NOT_EXIST, VALUE_TYPE_ERROR, OPERATOR_NOT_APPLICABLE

app = Flask(__name__)
mongo_db = Database()

DEFAULT_INPUT = -1
OK = 200
BAD_REQUEST = 400
NOT_FOUND = 404
UNSUPPORTED_MEDIA_TYPE = 415


@app.route('/')
def index():
    """
    Index page
    """
    return render_template('index.html')


@app.route('/get_or_delete')
def get_or_delete_page():
    """
    Page for Get or delete
    """
    return render_template('get_or_delete.html')


@app.route('/put_or_post')
def put_or_post_page():
    """
    Page for put or post
    """
    return render_template('put_or_post.html')


@app.route('/vis/top-authors')
def top_authors_page():
    """
    Page for get top k authors
    """
    return render_template('top_authors.html')


@app.route('/vis/top-books')
def top_books_page():
    """
    Page for get top k books
    """
    return render_template('top_books.html')


# http://127.0.0.1:5000/api/book?id={attr_value} Example: /book?id=3735293
@app.route('/api/book', methods=['GET'])
def get_book_by_id(book_id_input=DEFAULT_INPUT):
    """
    Get the book info by book id.
    Error should be reported with HTTP status code BAD_REQUEST if provided parameter is invalid.
    Error should be reported with HTTP status code NOT_FOUND if no such ID is found.

    Parameters:
    book_id_input (str): book id for api given from local
    """
    to_web = True
    if book_id_input != DEFAULT_INPUT:
        arg = book_id_input
        to_web = False
    else:
        arg = request.args.get('id')
    if not arg.isnumeric():
        return proceed_to_output({'GET error': f'Book id {arg} is not valid'}, BAD_REQUEST, to_web)
    book_id = arg
    book_doc = mongo_db.books_tb.find_one({'book_id': book_id}, {'_id': 0})
    if not book_doc:
        return proceed_to_output({'GET error': f'Book with id {book_id} is not found'},
                                 NOT_FOUND, to_web)
    # ready for service
    book = json.loads(dumps(book_doc))
    return proceed_to_output(book, OK, to_web)


# http://127.0.0.1:5000/api/author?id={attr_value} Example: /author?id=45372
@app.route('/api/author', methods=['GET'])
def get_author_by_id(author_id_input=DEFAULT_INPUT):
    """
    Get the author info by author id.
    Error should be reported with HTTP status code BAD_REQUEST if provided parameter is invalid.
    Error should be reported with HTTP status code NOT_FOUND if no such ID is found.

    Parameters:
    author_id_input (str): author id for api given from local
    """
    to_web = True
    if author_id_input != DEFAULT_INPUT:
        arg = author_id_input
        to_web = False
    else:
        arg = request.args.get('id')
    if not arg.isnumeric():
        return proceed_to_output({'GET error': f'Author id {arg} is not valid'},
                                 BAD_REQUEST, to_web)
    author_id = arg
    author_doc = mongo_db.authors_tb.find_one({'author_id': author_id}, {'_id': 0})
    if not author_doc:
        return proceed_to_output({'GET error': f'Author with id {author_id} is not found'},
                                 NOT_FOUND, to_web)
    # ready for service
    author = json.loads(dumps(author_doc))
    return proceed_to_output(author, OK, to_web)


# http://127.0.0.1:5000/api/search?q={query_string} Example: /search?q=book.id%3A123
@app.route('/api/search', methods=['GET'])
def get_by_query(query_string_input=DEFAULT_INPUT):
    """
    Get search results based on the specified query string.
    Errors should be reported if invalid search query.

    Parameters:
    query_string_input (str): query string for api given from local
    """
    to_web = True
    if query_string_input != DEFAULT_INPUT:
        query_string = query_string_input
        to_web = False
    else:
        query_string = request.args.get('q')
    # Parse and execute query string and get result documents
    documents = query(query_string, mongo_db)
    # Handle all the errors
    if documents is None:
        return proceed_to_output({'GET error': 'Result is not found in database'},
                                 NOT_FOUND, to_web)
    if documents == MALFORMED_QUERY_STRING:
        return proceed_to_output({'GET error': 'Malformed query strings'}, BAD_REQUEST, to_web)
    if documents == OBJECT_NOT_EXIST:
        return proceed_to_output({'GET error': 'Object in json is incorrect'}, BAD_REQUEST, to_web)
    if documents == FIELD_NOT_EXIST:
        return proceed_to_output({'GET error': 'Field in json is incorrect'}, BAD_REQUEST, to_web)
    if documents == VALUE_TYPE_ERROR:
        return proceed_to_output({'GET error': 'Value type of the field should be number'},
                                 BAD_REQUEST, to_web)
    if documents == OPERATOR_NOT_APPLICABLE:
        return proceed_to_output({'GET error': 'Comparison operators not applicable for string'},
                                 BAD_REQUEST, to_web)
    if documents.count() == 0:
        return proceed_to_output({'GET error': 'Result is not found in database'},
                                 NOT_FOUND, to_web)
    # Process output
    res = []
    for doc in documents:
        res.append(json.loads(dumps(doc)))
    return proceed_to_output(res, OK, to_web)


# http://127.0.0.1:5000/api/book?id={attr_value}
@app.route('/api/book', methods=['PUT'])
def put_book_by_id(book_id_input=DEFAULT_INPUT, json_file_input=DEFAULT_INPUT):
    """
    Put, or update book specified by the ID.
    Error should be reported with HTTP status code BAD_REQUEST if provided parameter is invalid.
    Error should be reported with HTTP status code NOT_FOUND if no such ID is found.
    Error should be reported with HTTP status code UNSUPPORTED_MEDIA_TYPE if content type header
    is not application/json.
    e.g. PUT {"ISBN": 1234567890} to /books?id=3735293 should update the ISBN value to that entry
    in the database.

    Parameters:
    book_id_input (str): book id for api given from local
    json_file_input (str): json file for api given from local
    """
    to_web = True
    if book_id_input != DEFAULT_INPUT:
        arg = book_id_input
        to_web = False
    else:
        arg = request.args.get('id')
    if not arg.isnumeric():
        return proceed_to_output({'PUT error': f'Book id {arg} is not valid'}, BAD_REQUEST, to_web)
    book_id = arg
    book_doc = mongo_db.books_tb.find_one({'book_id': book_id}, {'_id': 0})
    if not book_doc:
        return proceed_to_output({'PUT error': f'Book with id {book_id} is not found'},
                                 NOT_FOUND, to_web)
    # Load json content from correct position
    if json_file_input != DEFAULT_INPUT:
        with open(json_file_input, 'r') as file:
            try:
                json_content = json.load(file)
            except ValueError:
                return proceed_to_output('Invalid JSON file: File given is not a valid JSON file',
                                         BAD_REQUEST, to_web)
    else:
        if not is_content_type_json():
            return proceed_to_output({'PUT error': 'Content type header is not application/json'},
                                     UNSUPPORTED_MEDIA_TYPE, to_web)
        json_content = request.json
    book_dic = json.loads(dumps(json_content))
    if not isinstance(book_dic, dict):
        return proceed_to_output({'JSON structure error': 'Content of json is not a dict'},
                                 BAD_REQUEST, to_web)
    if not is_dict_value_type_valid(book_dic):
        return proceed_to_output({'JSON content error': 'Incorrect value type in json'},
                                 BAD_REQUEST, to_web)
    book_dic['book_id'] = book_id
    mongo_db.update_books_tb_from_json(book_dic)
    return proceed_to_output({'PUT success': f'Book with id {book_id} is updated'}, OK, to_web)


# http://127.0.0.1:5000/api/author?id={attr_value}
@app.route('/api/author', methods=['PUT'])
def put_author_by_id(author_id_input=DEFAULT_INPUT, json_file_input=DEFAULT_INPUT):
    """
    Put, or update author specified by the ID.
    Error should be reported with HTTP status code BAD_REQUEST if provided parameter is invalid.
    Error should be reported with HTTP status code NOT_FOUND if no such ID is found.
    Error should be reported with HTTP status code UNSUPPORTED_MEDIA_TYPE if content type header
    is not application/json.

    Parameters:
    author_id_input (str): author id for api given from local
    json_file_input (str): json file for api given from local
    """
    to_web = True
    if author_id_input != DEFAULT_INPUT:
        arg = author_id_input
        to_web = False
    else:
        arg = request.args.get('id')
    if not arg.isnumeric():
        return proceed_to_output({'PUT error': f'Author id {arg} is not valid'},
                                 BAD_REQUEST, to_web)
    author_id = arg
    author_doc = mongo_db.authors_tb.find_one({'author_id': author_id}, {'_id': 0})
    if not author_doc:
        return proceed_to_output({'PUT error': f'Author with id {author_id} is not found'},
                                 NOT_FOUND, to_web)
    # Load json content from correct position
    if json_file_input != DEFAULT_INPUT:
        with open(json_file_input, 'r') as file:
            try:
                json_content = json.load(file)
            except ValueError:
                return proceed_to_output('Invalid JSON file: File given is not a valid JSON file',
                                         BAD_REQUEST, to_web)
    else:
        if not is_content_type_json():
            return proceed_to_output({'PUT error': 'Content type header is not application/json'},
                                     UNSUPPORTED_MEDIA_TYPE, to_web)
        json_content = request.json
    author_dic = json.loads(dumps(json_content))
    if not isinstance(author_dic, dict):
        return proceed_to_output({'JSON structure error': 'Content of json is not a dict'},
                                 BAD_REQUEST, to_web)
    if not is_dict_value_type_valid(author_dic):
        return proceed_to_output({'JSON content error': 'Incorrect value type in json'},
                                 BAD_REQUEST, to_web)
    author_dic['author_id'] = author_id
    mongo_db.update_authors_tb_from_json(author_dic)
    return proceed_to_output({'PUT success': f'Author with id {author_id} is updated'}, OK, to_web)


# http://127.0.0.1:5000/api/book
@app.route('/api/book', methods=['POST'])
def post_book(json_file_input=DEFAULT_INPUT):
    """
    Leverage POST requests to ADD book to the backend (database).
    Error should be reported with HTTP status code BAD_REQUEST if book id already exists.
    Error should be reported with HTTP status code UNSUPPORTED_MEDIA_TYPE if content type header
    is not application/json.

    Parameters:
    json_file_input (str): json file for api given from local
    """
    to_web = True
    # Get json content
    if json_file_input != DEFAULT_INPUT:
        to_web = False
        with open(json_file_input, 'r') as file:
            try:
                json_content = json.load(file)
            except ValueError:
                return proceed_to_output('Invalid JSON file: File given is not a valid JSON file',
                                         BAD_REQUEST, to_web)
    else:
        if not is_content_type_json():
            return proceed_to_output({'POST error': 'Content type header is not application/json'},
                                     UNSUPPORTED_MEDIA_TYPE, to_web)
        json_content = request.json
    # ready for service
    response_dic = {}
    book_dic = json.loads(dumps(json_content))
    if not isinstance(book_dic, dict):
        # If JSON is not a dict, error
        response_dic['JSON structure error'] = 'Content of json is not a dict'
        return proceed_to_output(response_dic, BAD_REQUEST, to_web)
    if not is_dict_value_type_valid(book_dic):
        # If dict value is not valid, error
        response_dic['JSON content error'] = 'Incorrect value type in json'
        return proceed_to_output(response_dic, BAD_REQUEST, to_web)
    if 'book_id' not in book_dic.keys():
        # If 'book_id' is not found in dict keys, error
        response_dic['JSON structure error'] = 'Found book dict with no book id'
        return proceed_to_output(response_dic, BAD_REQUEST, to_web)
    book_id = book_dic['book_id']
    if not book_id:
        # If 'book_id' is empty, error
        response_dic['POST input error'] = 'Invalid book id'
        return proceed_to_output(response_dic, BAD_REQUEST, to_web)
    if mongo_db.is_book_exist(book_dic):
        # If value of 'book_id' already exists, error
        response_dic['POST input error'] = f'Book with id {book_id} already exists'
        return proceed_to_output(response_dic, BAD_REQUEST, to_web)
    # For the book, insert if id does not exist in database
    mongo_db.insert_books_tb_from_json(book_dic)
    response_dic['POST success'] = f'Book with id {book_id} is inserted'
    return proceed_to_output(response_dic, OK, to_web)


# http://127.0.0.1:5000/api/books
@app.route('/api/books', methods=['POST'])
def post_books(json_file_input=DEFAULT_INPUT):
    """
    Leverage POST requests to ADD books to the backend (database).
    Error should be reported if book id already exists.
    Error should be reported with HTTP status code UNSUPPORTED_MEDIA_TYPE if content type header
    is not application/json.

    Parameters:
    json_file_input (str): json file for api given from local
    """
    to_web = True
    # Get json content
    if json_file_input != DEFAULT_INPUT:
        to_web = False
        with open(json_file_input, 'r') as file:
            try:
                json_content = json.load(file)
            except ValueError:
                return proceed_to_output('Invalid JSON file: File given is not a valid JSON file',
                                         BAD_REQUEST, to_web)
    else:
        if not is_content_type_json():
            return proceed_to_output({'POST error': 'Content type header is not application/json'},
                                     UNSUPPORTED_MEDIA_TYPE, to_web)
        json_content = request.json
    # ready for service
    response_dic = {}
    array_books = json.loads(dumps(json_content))
    if not isinstance(array_books, list):
        # If JSON is not a list, return with message
        response_dic['JSON structure error'] = 'Content of json is not a list'
        return proceed_to_output(response_dic, BAD_REQUEST, to_web)
    for book_dic in array_books:
        # For every book, insert if id is found
        if 'book_id' not in book_dic.keys():
            response_dic['JSON structure error'] = 'Found book dict with no book id'
            continue
        if not is_dict_value_type_valid(book_dic):
            response_dic['JSON content error'] = 'Incorrect value type in json'
            continue
        book_id = book_dic['book_id']
        if not book_id:
            response_dic['POST input error'] = 'Invalid book id'
            continue
        if mongo_db.is_book_exist(book_dic):
            response_dic['POST input error'] = f'Book with id {book_id} already exists'
            continue
        mongo_db.insert_books_tb_from_json(book_dic)
        response_dic[f'POST {book_id} success'] = f'Book with id {book_id} is inserted'
    return proceed_to_output(response_dic, OK, to_web)


# http://127.0.0.1:5000/api/author
@app.route('/api/author', methods=['POST'])
def post_author(json_file_input=DEFAULT_INPUT):
    """
    Leverage POST requests to ADD author to the backend (database).
    Error should be reported with HTTP status code BAD_REQUEST if author id already exists.
    Error should be reported with HTTP status code UNSUPPORTED_MEDIA_TYPE if content type header
    is not application/json.

    Parameters:
    json_file_input (str): json file for api given from local
    """
    to_web = True
    # Get json content
    if json_file_input != DEFAULT_INPUT:
        to_web = False
        with open(json_file_input, 'r') as file:
            try:
                json_content = json.load(file)
            except ValueError:
                return proceed_to_output('Invalid JSON file: File given is not a valid JSON file',
                                         BAD_REQUEST, to_web)
    else:
        if not is_content_type_json():
            return proceed_to_output({'POST error': 'Content type header is not application/json'},
                                     UNSUPPORTED_MEDIA_TYPE, to_web)
        json_content = request.json
    # ready for service
    response_dic = {}
    author_dic = json.loads(dumps(json_content))
    if not isinstance(author_dic, dict):
        # If JSON is not a dict, error
        response_dic['JSON structure error'] = 'Content of json is not a dict'
        return proceed_to_output(response_dic, BAD_REQUEST, to_web)
    if not is_dict_value_type_valid(author_dic):
        # If dict value is not valid, error
        response_dic['JSON content error'] = 'Incorrect value type in json'
        return proceed_to_output(response_dic, BAD_REQUEST, to_web)
    if 'author_id' not in author_dic.keys():
        # If 'author_id' not in dict keys, error
        response_dic['JSON structure error'] = 'Found author dict with no author id'
        return proceed_to_output(response_dic, BAD_REQUEST, to_web)
    author_id = author_dic['author_id']
    if not author_id:
        # If 'author_id' is empty, error
        response_dic['POST input error'] = 'Invalid author id'
        return proceed_to_output(response_dic, BAD_REQUEST, to_web)
    if mongo_db.is_author_exist(author_dic):
        # If value of 'author_id' already exists, error
        response_dic['POST input error'] = f'Author with id {author_id} already exists'
        return proceed_to_output(response_dic, BAD_REQUEST, to_web)
    # For the author, insert if id does not exists in database
    mongo_db.insert_authors_tb_from_json(author_dic)
    response_dic['POST success'] = f'Author with id {author_id} is inserted'
    return proceed_to_output(response_dic, OK, to_web)


# http://127.0.0.1:5000/api/authors
@app.route('/api/authors', methods=['POST'])
def post_authors(json_file_input=DEFAULT_INPUT):
    """
    Leverage POST requests to ADD authors to the backend (database).
    Error should be reported if author id already exists.
    Error should be reported with HTTP status code UNSUPPORTED_MEDIA_TYPE if content type header
    is not application/json.

    Parameters:
    json_file_input (str): json file for api given from local
    """
    to_web = True
    # Get json content
    if json_file_input != DEFAULT_INPUT:
        to_web = False
        with open(json_file_input, 'r') as file:
            try:
                json_content = json.load(file)
            except ValueError:
                return proceed_to_output('Invalid JSON file: File given is not a valid JSON file',
                                         BAD_REQUEST, to_web)
    else:
        if not is_content_type_json():
            return proceed_to_output({'POST error': 'Content type header is not application/json'},
                                     UNSUPPORTED_MEDIA_TYPE, to_web)
        json_content = request.json
    # ready for service
    response_dic = {}
    array_authors = json.loads(dumps(json_content))
    if not isinstance(array_authors, list):
        # If JSON is not a list, return with message
        response_dic['JSON structure error'] = 'Content of json is not a list'
        return proceed_to_output(response_dic, BAD_REQUEST, to_web)
    for author_dic in array_authors:
        # For every book, insert if id is found
        if 'author_id' not in author_dic.keys():
            response_dic['JSON structure error'] = 'Found author dict with no author id'
            continue
        if not is_dict_value_type_valid(author_dic):
            response_dic['JSON content error'] = 'Incorrect value type in json'
            continue
        author_id = author_dic['author_id']
        if not author_id:
            response_dic['POST input error'] = 'Invalid author id'
            continue
        if mongo_db.is_author_exist(author_dic):
            response_dic['POST input error'] = f'Author with id {author_id} already exists'
            continue
        mongo_db.insert_authors_tb_from_json(author_dic)
        response_dic[f'POST {author_id} success'] = f'Author with id {author_id} is inserted'
    return proceed_to_output(response_dic, OK, to_web)


# http://127.0.0.1:5000/api/scrape?attr={attr_value}
@app.route('/api/scrape', methods=['POST'])
def post_scrape(url_input=DEFAULT_INPUT):
    """
    Scrape either authors or books and save the results in the database.
    Error should be reported with HTTP status code BAD_REQUEST if book/author id already exists.
    Error should be reported with HTTP status code UNSUPPORTED_MEDIA_TYPE if content type header
    is not application/json.
    URL parameters should be relative url of book and author page.
    e.g. /api/scrape?attr=book/show/3735293-clean-code

    Parameters:
    url_input (str): starting url for api given from local
    """
    to_web = True
    if url_input != DEFAULT_INPUT:
        to_web = False
        arg = url_input
    else:
        arg = request.args.get('attr')
    url_str = 'https://www.goodreads.com/' + arg
    # ready for service
    response_dic = {}
    if is_book(url_str):
        # scrape book page
        book_dic = scrape_book_page(url_str)[0]
        if book_dic is None:
            response_dic['POST scrape error'] = 'Book url given cannot be scraped'
            return proceed_to_output(response_dic, NOT_FOUND, to_web)
        book_id = book_dic['book_id']
        if mongo_db.is_book_exist(book_dic):
            response_dic['POST input error'] = f'Book with id {book_id} already exists'
            return proceed_to_output(response_dic, BAD_REQUEST, to_web)
        mongo_db.update_insert_books_tb(book_dic)
        response_dic['POST success'] = f'Book with id {book_id} is inserted'
    elif is_author(url_str):
        # scrape author page
        author_dic = scrape_author_page(url_str)[0]
        if author_dic is None:
            response_dic['POST scrape error'] = 'Author url given cannot be scraped'
            return proceed_to_output(response_dic, NOT_FOUND, to_web)
        author_id = author_dic['author_id']
        if mongo_db.is_author_exist(author_dic):
            response_dic['POST input error'] = f'Author with id {author_id} already exists'
            return proceed_to_output(response_dic, BAD_REQUEST, to_web)
        mongo_db.update_insert_authors_tb(author_dic)
        response_dic['POST success'] = f'Author with id {author_id} is inserted'
    else:
        # url invalid
        response_dic['POST error'] = 'URL is not a valid book/author page of Goodreads'
        return proceed_to_output(response_dic, BAD_REQUEST, to_web)
    return proceed_to_output(response_dic, OK, to_web)


# http://127.0.0.1:5000/api/book?id={attr_value} Example: /book?id=3735293
@app.route('/api/book', methods=['DELETE'])
def delete_book_by_id(book_id_input=DEFAULT_INPUT):
    """
    Delete book specified by the ID.
    Error should be reported with HTTP status code BAD_REQUEST if provided parameter is invalid.
    Error should be reported with HTTP status code NOT_FOUND if no such ID is found.

    Parameters:
    book_id_input (str): book id for api given from local
    """
    to_web = True
    if book_id_input != DEFAULT_INPUT:
        to_web = False
        arg = book_id_input
    else:
        arg = request.args.get('id')
    if not arg.isnumeric():
        return proceed_to_output({'DELETE error': f'Book id {arg} is not valid'},
                                 BAD_REQUEST, to_web)
    book_id = arg
    book_doc = mongo_db.books_tb.find_one({'book_id': book_id}, {'_id': 0})
    if not book_doc:
        return proceed_to_output({'DELETE error': f'Book with id {book_id} is not found'},
                                 NOT_FOUND, to_web)
    # ready for service
    mongo_db.books_tb.delete_one({'book_id': book_id})
    return proceed_to_output({'DELETE success': f'Book with id {book_id} is deleted'}, OK, to_web)


# http://127.0.0.1:5000/api/author?id={attr_value} Example: /author?id=45372
@app.route('/api/author', methods=['DELETE'])
def delete_author_by_id(author_id_input=DEFAULT_INPUT):
    """
    Delete author specified by the ID.
    Error should be reported with HTTP status code BAD_REQUEST if provided parameter is invalid.
    Error should be reported with HTTP status code NOT_FOUND if no such ID is found.

    Parameters:
    author_id_input (str): author id for api given from local
    """
    to_web = True
    if author_id_input != DEFAULT_INPUT:
        to_web = False
        arg = author_id_input
    else:
        arg = request.args.get('id')
    if not arg.isnumeric():
        return proceed_to_output({'DELETE error': f'Author id {arg} is not valid'},
                                 BAD_REQUEST, to_web)
    author_id = arg
    author_doc = mongo_db.authors_tb.find_one({'author_id': author_id}, {'_id': 0})
    if not author_doc:
        return proceed_to_output({'DELETE error': f'Author with id {author_id} is not found'},
                                 NOT_FOUND, to_web)
    # ready for service
    mongo_db.authors_tb.delete_one({'author_id': author_id})
    return proceed_to_output({'DELETE success': f'Author with id {author_id} is deleted'},
                             OK, to_web)


def is_content_type_json():
    """
    Check whether content type header is application/json
    """
    if request.content_type.startswith('application/json'):
        return True
    return False


def is_dict_value_type_valid(dic):
    """
    Check whether value type of the dict is string or list,
    and whether fields supposed to store number indeed store number.

    Parameters:
    dic (dict): dictionary given to check its value type
    """
    for key in dic:
        if not isinstance(dic[key], str) and not isinstance(dic[key], list):
            return False
        if check_content_type(key, dic[key]) == VALUE_TYPE_ERROR:
            return False
    return True


def proceed_to_output(response, status, to_web):
    """
    Return make_response if to_web is True, used in web api.
    Return a dict if to_web is False, used in local file.

    Parameters:
    response (dict): dictionary of response
    status (int): HTTP status code
    to_web (bool): whether the function should make response to web
    """
    if to_web:
        return make_response(jsonify(response), status)
    return response


if __name__ == '__main__':
    app.run(debug=True)
