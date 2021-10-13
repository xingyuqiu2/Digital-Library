"""
This module is test for database
"""
import unittest

from src.database import Database


class TestDatabase(unittest.TestCase):
    """
    Test class for methods in database
    """

    def test_is_book_exist(self):
        """
        Test method is_book_exist
        """
        self.assertFalse(database.is_book_exist(BOOK_DIC))

    def test_is_author_exist(self):
        """
        Test method is_author_exist
        """
        self.assertFalse(database.is_author_exist(AUTHOR_DIC))

    def test_update_insert_books_tb(self):
        """
        Test method update_insert_books_tb
        with helper function update_books_tb, insert_books_tb
        """
        # Test insert into books table
        database.update_insert_books_tb(BOOK_DIC)
        book_id = BOOK_DIC['book_id']
        self.assertNotEqual(None, database.books_tb.find_one({'book_id': book_id}))
        # Test update on books table
        new_book_dic = BOOK_DIC
        new_book_dic['title'] = 'New Book'
        database.update_insert_books_tb(new_book_dic)
        new_book = database.books_tb.find_one({'book_id': book_id})
        self.assertNotEqual(None, new_book)
        self.assertEqual('New Book', new_book['title'])

    def test_update_insert_authors_tb(self):
        """
        Test method update_insert_authors_tb
        with helper function update_authors_tb, insert_authors_tb
        """
        # Test insert into authors table
        database.update_insert_authors_tb(AUTHOR_DIC)
        author_id = AUTHOR_DIC['author_id']
        self.assertNotEqual(None, database.authors_tb.find_one({'author_id': author_id}))
        # Test update on authors table
        new_author_dic = AUTHOR_DIC
        new_author_dic['name'] = 'Tom'
        database.update_insert_authors_tb(new_author_dic)
        new_author = database.authors_tb.find_one({'author_id': author_id})
        self.assertNotEqual(None, new_author)
        self.assertEqual('Tom', new_author['name'])

    def test_update_insert_from_json_file(self):
        """
        Test method update_insert_from_json_file.
        Need a JSON file with name 'data.json' to test
        """
        json_file = 'src/data.json'
        database.update_insert_from_json_file(json_file)
        book_id = '3735293'
        new_book = database.books_tb.find_one({'book_id': book_id})
        self.assertNotEqual(None, new_book)
        self.assertEqual('Clean Code', new_book['title'])
        self.assertEqual('12345', new_book['ISBN'])
        self.assertEqual('5.0', new_book['rating'])
        author_id = '45372'
        new_author = database.authors_tb.find_one({'author_id': author_id})
        self.assertNotEqual(None, new_author)
        self.assertEqual('1000', new_author['review_count'])
        self.assertEqual(["CC", "TCC"], new_author['author_books'])


if __name__ == '__main__':
    database = Database()
    database.authors_tb.delete_many({})
    database.books_tb.delete_many({})
    BOOK_DIC = {'book_url': 'https://www.goodreads.com/book/show/3735293-clean-code',
                'title': 'Clean Code: A Handbook of Agile Software Craftsmanship',
                'book_id': '3735293',
                'ISBN': '0132350882',
                'author_url': 'https://www.goodreads.com/author/show/45372.Robert_C_Martin',
                'author': 'Robert C. Martin',
                'rating': '4.4',
                'rating_count': '1000',
                'review_count': '300',
                'image_url': 'https://i.gr-assets.com/images/12345.jpg',
                'similar_books': ['Book one', 'Book two']}
    AUTHOR_DIC = {'name': 'Robert C. Martin',
                  'author_url': 'https://www.goodreads.com/author/show/45372.Robert_C_Martin',
                  'author_id': '45372',
                  'rating': '4.34',
                  'rating_count': '31517',
                  'review_count': '2092',
                  'image_url': 'https://images.gr-assets.com/authors/1490470967p5/45372.jpg',
                  'related_authors': ['Andy Hunt', 'Steve McConnell'],
                  'author_books': ['Clean Code', 'The Clean Coder']}
    unittest.main()
