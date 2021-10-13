"""
This module is used to parse query string and execute query finding in database.
Program supports the following query string:
. operator to specify a field of an object. For example, book.rating_count
: operator to specify if a field contains search words. For example, book.book_id:123
"" operators to specify the exact search term. For example, book.image_url:"123"
AND, OR, and NOT logical operators. For example, book.rating_count: NOT 123
One-side unbounded comparison operators >, <. For example, book.rating_count: > 123
"""
from src.database import BOOK_ATTRIBUTES, AUTHOR_ATTRIBUTES

BOOK_STR = 'book'
AUTHOR_STR = 'author'
LOGICAL_OPERATORS = ['AND', 'OR']
SIGNS = ['$and', '$or']
BOOK_QUERY = 2
AUTHOR_QUERY = 3
NOT_EXIST = -1
CAN_BE_COMPARED = 1
CANNOT_BE_COMPARED = 0
MALFORMED_QUERY_STRING = -1
OBJECT_NOT_EXIST = -2
FIELD_NOT_EXIST = -3
VALUE_TYPE_ERROR = -4
OPERATOR_NOT_APPLICABLE = -5


def query(query_string, mongo_db):
    """
    Query the database and return cursor according to the query.
    If error happens during the process, then related error is returned.

    Parameters:
    query_string (str): query string for search
    mongo_db (object): database object
    """
    has_logical_operator = False
    for operator in LOGICAL_OPERATORS:
        if query_string.find(operator) != NOT_EXIST:
            has_logical_operator = True
    if has_logical_operator:
        # need to first divide at AND/OR, then parse
        res = divide_query_string_and_parse(query_string)
    else:
        # parse directly
        res = parse_single_query(query_string)
    # check error
    if is_error_occur(res):
        return res
    # process the query and return cursor
    query_type, my_query = res
    if query_type == BOOK_QUERY:
        return mongo_db.books_tb.find(my_query, {'_id': 0})
    return mongo_db.authors_tb.find(my_query, {'_id': 0})


def divide_query_string_and_parse(query_string):
    """
    Divide query string into two query at AND/OR.
    Then parse the query separately.
    Check error after calling each helper functions.

    Parameters:
    query_string (str): query string for search
    """
    for i, logical_operator in enumerate(LOGICAL_OPERATORS):
        if query_string.find(logical_operator) != NOT_EXIST:
            first_query, second_query = query_string.split(logical_operator)
            first_query = first_query.strip()
            second_query = second_query.strip()
            # parse first query
            first_parts = parser(first_query)
            if is_error_occur(first_parts):
                return first_parts
            first_obj, first_field, first_content = first_parts
            # parse second query
            second_parts = parser(second_query)
            if is_error_occur(second_parts):
                return second_parts
            second_obj, second_field, second_content = second_parts
            # check object and field not exist error
            query_type = check_obj_and_field(first_obj, first_field, second_obj, second_field)
            if is_error_occur(query_type):
                return query_type
            # process the content
            first_condition = content_to_query(first_field, first_content)
            if is_error_occur(first_condition):
                return first_condition
            second_condition = content_to_query(second_field, second_content)
            if is_error_occur(second_condition):
                return second_condition
            # Get the query and return
            my_query = {SIGNS[i]: [first_condition, second_condition]}
            return query_type, my_query


def parse_single_query(query_string):
    """
    Parse the query directly.
    Check error after calling each helper functions.

    Parameters:
    query_string (str): query string for search
    """
    parts = parser(query_string)
    if is_error_occur(parts):
        return parts
    obj, field, content = parts
    # Check object, field not exist error
    if obj == BOOK_STR:
        if field not in BOOK_ATTRIBUTES:
            return FIELD_NOT_EXIST
        my_query = content_to_query(field, content)
        if is_error_occur(my_query):
            return my_query
        return BOOK_QUERY, my_query
    if obj == AUTHOR_STR:
        if field not in AUTHOR_ATTRIBUTES:
            return FIELD_NOT_EXIST
        my_query = content_to_query(field, content)
        if is_error_occur(my_query):
            return my_query
        return AUTHOR_QUERY, my_query
    # object is not valid
    return OBJECT_NOT_EXIST


def check_obj_and_field(first_obj, first_field, second_obj, second_field):
    """
    Check validity of object and field for query with AND/OR.
    Return error if any.
    Otherwise, return the type of query: BOOK_QUERY/AUTHOR_QUERY

    Parameters:
    first_obj (str): first object in query string
    first_field (str): first field in query string
    second_obj (str): second object in query string
    second_field (str): second field in query string
    """
    if first_obj == BOOK_STR:
        if second_obj != BOOK_STR:
            return OBJECT_NOT_EXIST
        if first_field not in BOOK_ATTRIBUTES:
            return FIELD_NOT_EXIST
        if second_field not in BOOK_ATTRIBUTES:
            return FIELD_NOT_EXIST
        return BOOK_QUERY
    if first_obj == AUTHOR_STR:
        if second_obj != AUTHOR_STR:
            return OBJECT_NOT_EXIST
        if first_field not in AUTHOR_ATTRIBUTES:
            return FIELD_NOT_EXIST
        if second_field not in AUTHOR_ATTRIBUTES:
            return FIELD_NOT_EXIST
        return AUTHOR_QUERY
    # object is not valid
    return OBJECT_NOT_EXIST


def parser(query_string):
    """
    Parse the query string and separate it by the format 'object.field:content' into three section.
    Error MALFORMED_QUERY_STRING is returned if '.' or ':' is not found.

    Parameters:
    query_string (str): query string for search
    """
    # Split once from .
    try:
        obj, rest_string = query_string.split('.', 1)
    except ValueError:
        return MALFORMED_QUERY_STRING
    # Split once from :
    try:
        field, content = rest_string.split(':', 1)
    except ValueError:
        return MALFORMED_QUERY_STRING
    return obj.strip(), field.strip(), content.strip()


def content_to_query(field, content):
    """
    Convert content section into query which is used in mongo_db.collection.find().
    NOT logical operators. For example, book.rating_count: NOT 123.
    One-side unbounded comparison operators <, >. For example, book.rating_count: > 123.
    Single content without operators. For example, book.book_id: 123.

    Parameters:
    field (str): field string in query string
    content (str): content string in query string
    """
    if content.find('NOT') != NOT_EXIST:
        not_content = content.split('NOT')[1].strip()
        type_check = check_content_type(field, not_content)
        if is_error_occur(type_check):
            return type_check
        return {field: {'$ne': not_content}}
    if content.find('<') != NOT_EXIST:
        lt_content = content.split('<')[1]
        type_check = check_content_type(field, lt_content)
        if is_error_occur(type_check):
            return type_check
        if type_check == CANNOT_BE_COMPARED:
            return OPERATOR_NOT_APPLICABLE
        return {'$expr': {'$lt': [{'$toDouble': f'${field}'}, float(lt_content)]}}
    if content.find('>') != NOT_EXIST:
        gt_content = content.split('>')[1]
        type_check = check_content_type(field, gt_content)
        if is_error_occur(type_check):
            return type_check
        if type_check == CANNOT_BE_COMPARED:
            return OPERATOR_NOT_APPLICABLE
        return {'$expr': {'$gt': [{'$toDouble': f'${field}'}, float(gt_content)]}}
    # single content
    type_check = check_content_type(field, content)
    if is_error_occur(type_check):
        return type_check
    condition = condition_single_content(content)
    return {field: condition}


def condition_single_content(content):
    """
    Handle query for single content.
    Return condition in query, flag of whether to add field as key

    Parameters:
    content (str): content string in query string without operators
    """
    content = content.strip()
    # query exact search term
    if content and content[0] == '"' and content[-1] == '"':
        content = content[1:-1]
        return content
    # query field that contains search words
    return {'$regex': '.*' + content + '.*'}


def check_content_type(field, content):
    """
    Check the type of content corresponding to the field.
    If type of content is not correct, VALUE_TYPE_ERROR is returned.
    If type can be compared, return CAN_BE_COMPARED.
    Otherwise, return CANNOT_BE_COMPARED.

    Parameters:
    field (str): field string in query string
    content (str): content string in query string without operators
    """
    content = content.strip()
    if not content:
        return CANNOT_BE_COMPARED
    has_quote = False
    if content[0] == '"' and content[-1] == '"':
        content = content[1:-1]
        has_quote = True
    if field in {'book_id', 'author_id' , 'rating_count', 'review_count'}:
        # Content value for these field should be integer
        if not content.isnumeric():
            return VALUE_TYPE_ERROR
        if not has_quote:
            return CAN_BE_COMPARED
    if field == 'rating':
        # Content value for this field should be float
        try:
            float(content)
        except ValueError:
            return VALUE_TYPE_ERROR
        else:
            if not has_quote:
                return CAN_BE_COMPARED
    # Value of other fields is not int or float, cannot be compared
    return CANNOT_BE_COMPARED


def is_error_occur(return_value):
    """
    Check whether error has occurred by the return value.

    Parameters:
    return_value: value returned from functions in this file
    """
    if isinstance(return_value, int) \
            and OPERATOR_NOT_APPLICABLE <= return_value <= MALFORMED_QUERY_STRING:
        return True
    return False
