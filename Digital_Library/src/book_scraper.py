"""
This module contains methods to scrape book attributes from a book page.
"""
from urllib.request import urlopen
import logging

from bs4 import BeautifulSoup


def scrape_book_page(book_url):
    """
    Scrape the book page and create book instance
    Return the book and similar books' urls
    """
    soup = get_soup(book_url)
    if soup is None:
        return None, []
    title = find_title(soup)
    book_id = find_book_id(book_url)
    isbn = find_isbn(soup)
    author_url, author = find_author_url_and_name(soup)
    rating, rating_count, review_count = find_book_meta(soup)
    image_url = find_image_url(soup)
    similar_books_names, similar_books_urls = find_similar_books_and_urls(soup)
    j_dic = {'book_url': book_url, 'title': title, 'book_id': book_id,
             'ISBN': isbn, 'author_url': author_url, 'author': author,
             'rating': rating, 'rating_count': rating_count,
             'review_count': review_count, 'image_url': image_url,
             'similar_books': similar_books_names}
    return j_dic, similar_books_urls


def get_soup(url):
    """
    Get the soup by book url
    """
    try:
        book_html = urlopen(url)
    except:
        logging.error('Cannot open book_url')
        return None
    return BeautifulSoup(book_html, 'html.parser')


def find_title(soup):
    """
    Find the title of the book
    """
    title = ''
    title_holder = soup.find('h1', class_='gr-h1 gr-h1--serif')
    if title_holder is None:
        logging.error('Error in finding title')
        return title
    title = title_holder.text.strip()
    return title


def find_book_id(book_url):
    """
    Find the book id of the book
    """
    book_id = ''
    for char in book_url[36:]:
        if not char.isdigit():
            break
        book_id += char
    return book_id


def find_isbn(soup):
    """
    Find the ISBN of the book
    """
    isbn = ''
    details_holder = soup.find(id='details').find('div', class_='buttons')
    details = details_holder.find_all('div', class_='clearFloats')
    # check if we can find ISBN title
    for detail in details:
        isbn_title_holder = detail.find('div', class_='infoBoxRowTitle')
        if isbn_title_holder is None:
            logging.error('Error in finding ISBN title')
            return isbn
        isbn_title = isbn_title_holder.text.strip()
        if isbn_title != 'ISBN':
            # no ISBN in this line
            continue
        # check if we can find ISBN
        isbn_holder = detail.find('div', class_='infoBoxRowItem')
        if isbn_holder is None:
            logging.error('Error in finding ISBN')
            return isbn
        isbn = isbn_holder.text.strip()
        # get ISBN without ISBN13 in the bracket
        end_i = 0
        for i, char in enumerate(isbn):
            if char == '(':
                end_i = i
                break
        isbn = isbn[:end_i].strip()
        break
    return isbn


def find_author_url_and_name(soup):
    """
    Find the author url and name
    """
    author_holder = soup.find(id='bookAuthors').find('a', class_='authorName')
    if author_holder is None:
        logging.error('Error in finding book author url and name')
        return '', ''
    author_url = author_holder['href']
    author = author_holder.text.strip()
    return author_url, author


def find_book_meta(soup):
    """
    Find the rating, rating count, and review count of the book
    """
    rating = ''
    rating_count = ''
    review_count = ''
    book_meta_holder = soup.find(id='bookMeta')
    if book_meta_holder is None:
        logging.error('Error in finding book meta')
        return rating, rating_count, review_count

    # find rating
    rating_holder = book_meta_holder.find(itemprop='ratingValue')
    if rating_holder is None:
        logging.error('Error in finding book rating')
        return rating, rating_count, review_count
    rating = rating_holder.text.strip()

    # find rating_count
    rating_count_holder = book_meta_holder.find(itemprop='ratingCount')
    if rating_count_holder is None:
        logging.error('Error in finding book rating count')
        return rating, rating_count, review_count
    rating_count_text = rating_count_holder.text.strip()
    # get the digit in text and append it to rating_count
    for char in rating_count_text:
        if char.isdigit():
            rating_count += char

    # find review_count
    review_count_holder = book_meta_holder.find(itemprop='reviewCount')
    if review_count_holder is None:
        logging.error('Error in finding book review count')
        return rating, rating_count, review_count
    review_count_text = review_count_holder.text.strip()
    # get the digit in text and append it to review_count
    for char in review_count_text:
        if char.isdigit():
            review_count += char
    return rating, rating_count, review_count


def find_image_url(soup):
    """
    Find the image url of the book
    """
    image_url_holder = soup.find('div', class_='bookCoverPrimary').find(id='coverImage')
    if image_url_holder is None:
        logging.error('Error in finding book image url')
        return ''
    image_url = image_url_holder['src']
    return image_url


def find_similar_books_and_urls(soup):
    """
    Find the similar books' titles and urls
    """
    similar_books_names = []
    similar_books_urls = []
    similar_books_link_holder = soup.find('a', class_='actionLink right seeMoreLink')
    if similar_books_link_holder is None:
        logging.error('Cannot find similar books link')
        return similar_books_names, similar_books_urls
    similar_books_link = similar_books_link_holder['href']

    try:
        similar_books_html = urlopen(similar_books_link)
    except:
        logging.error('Cannot open similar books link')
        return similar_books_names, similar_books_urls

    new_soup = BeautifulSoup(similar_books_html, 'html.parser')
    similar_book_info_holders = new_soup.find_all('a', class_='gr-h3 gr-h3--serif gr-h3--noMargin')
    for similar_book_info_holder in similar_book_info_holders:
        rel_similar_book_url = similar_book_info_holder['href']
        similar_book_url = 'https://www.goodreads.com' + rel_similar_book_url
        similar_book_name_holder = similar_book_info_holder.find(itemprop='name')
        similar_books_urls.append(similar_book_url)
        similar_books_names.append(similar_book_name_holder.text.strip())
    return similar_books_names[1:], similar_books_urls[1:]


def is_book(url):
    """
    Check whether url is a book page in GoodReads
    """
    if url[:36] != 'https://www.goodreads.com/book/show/':
        return False
    soup = get_soup(url)
    if soup is None:
        return False
    if soup.find(id='bookTitle'):
        return True
    return False
