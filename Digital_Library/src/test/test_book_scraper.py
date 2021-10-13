"""
This module is test for book_scraper
"""
import unittest

from src.book_scraper import is_book
from src.book_scraper import get_soup
from src.book_scraper import find_title
from src.book_scraper import find_author_url_and_name
from src.book_scraper import find_book_id
from src.book_scraper import find_book_meta
from src.book_scraper import find_image_url
from src.book_scraper import find_isbn
from src.book_scraper import find_similar_books_and_urls


class TestBookScraper(unittest.TestCase):
    """
    Test class for book_scraper
    """

    def test_is_book(self):
        """
        Test method is_book
        """
        other_url = 'https://www.youtube.com/'
        author_url = 'https://www.goodreads.com/author/show/45372.Robert_C_Martin'
        invalid_book_url = 'https://www.goodreads.com/book/show/Software_Estimation'
        self.assertFalse(is_book(other_url))
        self.assertTrue(is_book(BOOK_URL))
        self.assertFalse(is_book(author_url))
        self.assertFalse(is_book(invalid_book_url))

    def test_find_title(self):
        """
        Test method find_title
        """
        title = find_title(soup)
        self.assertEqual('Software Estimation: Demystifying the Black Art', title)

    def test_find_book_id(self):
        """
        Test method find_book_id
        """
        book_id = find_book_id(BOOK_URL)
        self.assertEqual('93891', book_id)

    def test_find_isbn(self):
        """
        Test method find_isbn
        """
        isbn = find_isbn(soup)
        self.assertEqual('0735605351', isbn)

    def test_find_author_url_and_name(self):
        """
        Test method find_author_url_and_name
        """
        author_url, name = find_author_url_and_name(soup)
        self.assertEqual('https://www.goodreads.com/author/show/3307.Steve_McConnell', author_url)
        self.assertEqual('Steve McConnell', name)

    def test_find_book_meta(self):
        """
        Test method find_book_meta
        """
        rating, rating_count, review_count = find_book_meta(soup)
        self.assertNotEqual(-1.0, rating)
        self.assertNotEqual(-1, rating_count)
        self.assertNotEqual(-1, review_count)

    def test_find_image_url(self):
        """
        Test method find_image_url
        """
        image_url = find_image_url(soup)
        exp_url = 'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1396830924l/93891.jpg'
        self.assertEqual(exp_url, image_url)

    def test_find_similar_books_and_urls(self):
        """
        Test method find_similar_books_and_urls
        """
        similar_books_names, similar_books_urls = find_similar_books_and_urls(soup)
        self.assertEqual('The Mythical Man-Month: Essays on Software Engineering',
                         similar_books_names[0])
        self.assertEqual('https://www.goodreads.com/book/show/13629.The_Mythical_Man_Month',
                         similar_books_urls[0])


if __name__ == '__main__':
    BOOK_URL = 'https://www.goodreads.com/book/show/93891.Software_Estimation'
    soup = get_soup(BOOK_URL)
    unittest.main()
