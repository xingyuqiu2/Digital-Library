"""
This module is test for web api
"""
import unittest
import requests

from src.library_app import mongo_db

BASE = 'http://127.0.0.1:5000/'


class TestApi(unittest.TestCase):
    """
    Test class for library_app.py
    """

    def test_get_book_by_id(self):
        """
        Test GET api/book?id={attr_value}
        """
        response = requests.get(BASE + 'api/book?id=123')
        self.assertEqual(404, response.status_code)

        url = 'book/show/44936.Refactoring'
        requests.post(BASE + 'api/scrape?attr=' + url)
        response = requests.get(BASE + 'api/book?id=44936')
        self.assertEqual(200, response.status_code)

    def test_get_author_by_id(self):
        """
        Test GET api/author?id={attr_value}
        """
        response = requests.get(BASE + 'api/author?id=123')
        self.assertEqual(404, response.status_code)

        url = 'author/show/45372.Robert_C_Martin'
        requests.post(BASE + 'api/scrape?attr=' + url)
        response = requests.get(BASE + 'api/author?id=45372')
        self.assertEqual(200, response.status_code)

    def test_get_by_query_basic(self):
        """
        Test GET api/search?q={query_string} with
        format of object.field:content
        """
        json_content = {'book_id': '1024', 'title': 'test basic query book'}
        requests.post(BASE + 'api/book', json=json_content)

        response = requests.get(BASE + 'api/search?q=book_id in book:1024')
        self.assertEqual(400, response.status_code)

        response = requests.get(BASE + 'api/search?q=dog.book_id:256')
        self.assertEqual(400, response.status_code)

        response = requests.get(BASE + 'api/search?q=book.book_id:256')
        self.assertEqual(404, response.status_code)

        response = requests.get(BASE + 'api/search?q=book.book_id:10')
        self.assertEqual(200, response.status_code)

    def test_get_by_query_quote(self):
        """
        Test GET api/search?q={query_string} with
        "" operators to specify the exact search term.
        """
        json_content = {'book_id': '2048', 'title': 'test quote book'}
        requests.post(BASE + 'api/book', json=json_content)

        response = requests.get(BASE + 'api/search?q=book.book_id:"20"')
        self.assertEqual(404, response.status_code)

        response = requests.get(BASE + 'api/search?q=book.book_id:"2048"')
        self.assertEqual(200, response.status_code)

    def test_get_by_query_logical_operator(self):
        """
        Test GET api/search?q={query_string} with
        AND, OR, and NOT logical operators.
        """
        mongo_db.authors_tb.delete_many({})
        mongo_db.books_tb.delete_many({})
        json_content = [{'book_id': '4096', 'title': 'test logical operator book', 'ISBN': '33'},
                        {'book_id': '5096', 'ISBN': '666777'}]
        requests.post(BASE + 'api/books', json=json_content)

        response = requests.get(BASE + 'api/search?q=book.title:test AND author.name:no')
        self.assertEqual(400, response.status_code)

        response = requests.get(BASE + 'api/search?q=book.title:test AND book.ISBN:3')
        self.assertEqual(200, response.status_code)

        response = requests.get(BASE + 'api/search?q=book.title:none OR book.ISBN:67')
        self.assertEqual(200, response.status_code)

        response = requests.get(BASE + 'api/search?q=book.book_id:NOT 4096ANDbook.book_id:NOT 5096')
        self.assertEqual(404, response.status_code)

    def test_get_by_query_comparison_operator(self):
        """
        Test GET api/search?q={query_string} with
        one-side unbounded comparison operators <, >.
        """
        mongo_db.authors_tb.delete_many({})
        mongo_db.books_tb.delete_many({})
        json_content = [{'author_id': '8848', 'name': 'test comparison 1', 'rating': '4.5'},
                        {'author_id': '9981', 'name': 'test comparison 2', 'rating': '3.5'}]
        requests.post(BASE + 'api/authors', json=json_content)

        response = requests.get(BASE + 'api/search?q=author.rating:>4.4')
        self.assertEqual(200, response.status_code)

        response = requests.get(BASE + 'api/search?q=author.rating: < 0.5')
        self.assertEqual(404, response.status_code)

        response = requests.get(BASE + 'api/search?q=author.name: > eee')
        self.assertEqual(400, response.status_code)

    def test_put_book_by_id(self):
        """
        Test PUT api/book?id={attr_value}
        """
        json_content = {'book_id': '85009', 'title': 'Design_Patterns'}
        requests.post(BASE + 'api/book', json=json_content)

        json_content = {'ISBN': '5656', 'rating': 'letter'}
        response = requests.put(BASE + 'api/book?id=85009', json=json_content)
        self.assertEqual(400, response.status_code)

        json_content = {'ISBN': '5656', 'rating': '5.0'}
        response = requests.put(BASE + 'api/book?id=85009', json=json_content)
        self.assertEqual(200, response.status_code)

    def test_put_author_by_id(self):
        """
        Test PUT api/author?id={attr_value}
        """
        json_content = {'author_id': '2815', 'name': 'Andy Hunt'}
        requests.post(BASE + 'api/author', json=json_content)

        json_content = {'name': 'ME', 'rating': '5.0'}
        response = requests.put(BASE + 'api/author?id=1111', json=json_content)
        self.assertEqual(404, response.status_code)

        response = requests.put(BASE + 'api/author?id=2815', json=json_content)
        self.assertEqual(200, response.status_code)

    def test_post_book(self):
        """
        Test POST api/book
        """
        json_content = {'title': 'My Book', 'rating': '4.9'}
        response = requests.post(BASE + 'api/book', json=json_content)
        self.assertEqual(400, response.status_code)

        json_content = {'book_id': '555', 'title': 'My Book', 'rating': '4.9'}
        response = requests.post(BASE + 'api/book', json=json_content)
        self.assertEqual(200, response.status_code)

    def test_post_books(self):
        """
        Test POST api/books
        """
        json_content = {'book_id': '666', 'title': 'My Book'}
        response = requests.post(BASE + 'api/books', json=json_content)
        self.assertEqual(400, response.status_code)

        json_content = [{'book_id': '666', 'title': 'My Book'},
                        {'book_id': '777', 'title': 'Another Book'}]
        response = requests.post(BASE + 'api/books', json=json_content)
        self.assertEqual(200, response.status_code)

    def test_post_author(self):
        """
        Test POST api/author
        """
        json_content = {'name': 'Tom', 'rating': '2.5'}
        response = requests.post(BASE + 'api/author', json=json_content)
        self.assertEqual(400, response.status_code)

        json_content = {'author_id': '22', 'name': 'Tom', 'rating': '2.5'}
        response = requests.post(BASE + 'api/author', json=json_content)
        self.assertEqual(200, response.status_code)

    def test_post_authors(self):
        """
        Test POST api/authors
        """
        json_content = {'author_id': '33', 'name': 'Dude', 'rating': '3.5'}
        response = requests.post(BASE + 'api/authors', json=json_content)
        self.assertEqual(400, response.status_code)

        json_content = [{'author_id': '33', 'name': 'Dude', 'rating': '3.5'},
                        {'author_id': '44', 'name': 'Mate', 'rating': '4.0'}]
        response = requests.post(BASE + 'api/authors', json=json_content)
        self.assertEqual(200, response.status_code)

    def test_post_scrape(self):
        """
        Test POST api/scrape?attr={attr_value}
        """
        url = 'book/show/3735293-clean-code'
        response = requests.post(BASE + 'api/scrape?attr=' + url)
        self.assertEqual(200, response.status_code)
        self.assertTrue(mongo_db.books_tb.find_one({'book_id': '3735293'}))

    def test_delete_book_by_id(self):
        """
        Test DELETE api/book?id={attr_value}
        """
        json_content = {'book_id': '88', 'title': 'My Book to delete', 'rating': '1.1'}
        requests.post(BASE + 'api/book', json=json_content)

        response = requests.delete(BASE + 'api/book?id=88')
        self.assertEqual(200, response.status_code)

        response = requests.delete(BASE + 'api/book?id=88')
        self.assertEqual(404, response.status_code)

    def test_delete_author_by_id(self):
        """
        Test DELETE api/author?id={attr_value}
        """
        json_content = {'author_id': '78', 'name': 'Bye Bye', 'rating': '0.9'}
        requests.post(BASE + 'api/author', json=json_content)

        response = requests.delete(BASE + 'api/author?id=78')
        self.assertEqual(200, response.status_code)

        response = requests.delete(BASE + 'api/author?id=78')
        self.assertEqual(404, response.status_code)


if __name__ == '__main__':
    mongo_db.authors_tb.delete_many({})
    mongo_db.books_tb.delete_many({})
    unittest.main()
