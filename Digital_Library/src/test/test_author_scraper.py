"""
This module is test for author_scraper
"""
import unittest

from src.author_scraper import is_author
from src.author_scraper import get_soup
from src.author_scraper import find_name
from src.author_scraper import find_author_id
from src.author_scraper import find_author_meta
from src.author_scraper import find_image_url
from src.author_scraper import find_related_authors_and_urls
from src.author_scraper import find_author_books


class TestAuthorScraper(unittest.TestCase):
    """
    Test class for author_scraper
    """

    def test_is_author(self):
        """
        Test method is_author
        """
        other_url = 'https://www.youtube.com/'
        book_url = 'https://www.goodreads.com/book/show/93891.Software_Estimation'
        author_url1 = 'https://www.goodreads.com/author/show/3307.Steve_McConnell'
        invalid_author_url = 'https://www.goodreads.com/author/show/Tom_DeMarco'
        self.assertFalse(is_author(other_url))
        self.assertTrue(is_author(AUTHOR_URL))
        self.assertFalse(is_author(book_url))
        self.assertTrue(is_author(author_url1))
        self.assertFalse(is_author(invalid_author_url))

    def test_find_name(self):
        """
        Test method find_name
        """
        name = find_name(soup)
        self.assertEqual('Robert C. Martin', name)

    def test_find_author_id(self):
        """
        Test method find_author_id
        """
        author_id = find_author_id(AUTHOR_URL)
        self.assertEqual('45372', author_id)

    def test_find_author_meta(self):
        """
        Test method find_author_meta
        """
        rating, rating_count, review_count = find_author_meta(soup)
        self.assertNotEqual(-1.0, rating)
        self.assertNotEqual(-1, rating_count)
        self.assertNotEqual(-1, review_count)

    def test_find_image_url(self):
        """
        Test method find_image_url
        """
        image_url = find_image_url(soup)
        self.assertEqual('https://images.gr-assets.com/authors/1490470967p5/45372.jpg', image_url)

    def test_find_related_authors_and_urls(self):
        """
        Test method find_related_authors_and_urls
        """
        related_authors, related_authors_urls = find_related_authors_and_urls(soup)
        self.assertEqual('Andy Hunt', related_authors[0])
        self.assertEqual('https://www.goodreads.com/author/show/2815.Andy_Hunt',
                         related_authors_urls[0])

    def test_find_author_books(self):
        """
        Test method find_author_books
        """
        author_books = find_author_books(soup)
        self.assertEqual('Clean Code: A Handbook of Agile Software Craftsmanship', author_books[0])


if __name__ == '__main__':
    AUTHOR_URL = 'https://www.goodreads.com/author/show/45372.Robert_C_Martin'
    soup = get_soup(AUTHOR_URL)
    unittest.main()
