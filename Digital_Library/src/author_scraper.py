"""
This module contains methods to scrape author attributes from a author page.
"""
from urllib.request import urlopen
import logging

from bs4 import BeautifulSoup


def scrape_author_page(author_url):
    """
    Scrape the author page and create author instance
    Return the author and related authors' urls
    """
    soup = get_soup(author_url)
    if soup is None:
        return None, []
    name = find_name(soup)
    author_id = find_author_id(author_url)
    rating, rating_count, review_count = find_author_meta(soup)
    image_url = find_image_url(soup)
    related_authors, related_authors_urls = find_related_authors_and_urls(soup)
    author_books = find_author_books(soup)
    j_dic = {'name': name, 'author_url': author_url, 'author_id': author_id,
             'rating': rating, 'rating_count': rating_count,
             'review_count': review_count, 'image_url': image_url,
             'related_authors': related_authors, 'author_books': author_books}
    return j_dic, related_authors_urls


def get_soup(author_url):
    """
    Get the soup by author url
    """
    try:
        author_html = urlopen(author_url)
    except:
        logging.error('Cannot open author_url')
        return None
    return BeautifulSoup(author_html, 'html.parser')


def find_name(soup):
    """
    Find the name of the author
    """
    name = ''
    name_holder = soup.find('div', class_='leftContainer authorLeftContainer').find('img')
    if name_holder is None:
        logging.error('Error in finding author name')
        return name
    name = name_holder['alt'].strip()
    return name


def find_author_id(author_url):
    """
    Find the author id of author
    """
    author_id = ''
    for char in author_url[38:]:
        if not char.isdigit():
            break
        author_id += char
    return author_id


def find_author_meta(soup):
    """
    Find the rating, rating count, and review count of the author
    """
    rating = ''
    rating_count = ''
    review_count = ''
    author_meta_holder = soup.find('div', class_='hreview-aggregate')
    if author_meta_holder is None:
        logging.error('Error in finding author meta')
        return rating, rating_count, review_count

    # find rating
    rating_holder = author_meta_holder.find(itemprop='ratingValue')
    if rating_holder is None:
        logging.error('Error in finding author rating')
        return rating, rating_count, review_count
    rating = rating_holder.text.strip()

    # find rating_count
    rating_count_holder = author_meta_holder.find(itemprop='ratingCount')
    if rating_count_holder is None:
        logging.error('Error in finding author rating count')
        return rating, rating_count, review_count
    rating_count_text = rating_count_holder.text.strip()
    # get the digit in text and append it to rating_count
    for char in rating_count_text:
        if char.isdigit():
            rating_count += char

    # find review_count
    review_count_holder = author_meta_holder.find(itemprop='reviewCount')
    if review_count_holder is None:
        logging.error('Error in finding author review count')
        return rating, rating_count, review_count
    review_count_text = review_count_holder.text.strip()
    # get the digit in text and append it to review_count
    for char in review_count_text:
        if char.isdigit():
            review_count += char
    return rating, rating_count, review_count


def find_image_url(soup):
    """
    Find the image url of the author
    """
    image_url_holder = soup.find('div', class_='leftContainer authorLeftContainer').find('img')
    if image_url_holder is None:
        logging.error('Error in finding author image url')
        return ''
    image_url = image_url_holder['src']
    return image_url


def find_related_authors_and_urls(soup):
    """
    Find the related authors' names and urls
    """
    related_authors = []
    related_authors_urls = []
    author_meta_holder = soup.find('div', class_='hreview-aggregate')
    if author_meta_holder is None:
        logging.error('Error in finding author meta')
        return related_authors, related_authors_urls
    related_authors_link = ''
    for related_authors_link_holder in author_meta_holder.find_all('a'):
        if related_authors_link_holder.text.strip() == 'Similar authors':
            rel_related_authors_link = related_authors_link_holder['href']
            related_authors_link = 'https://www.goodreads.com' + rel_related_authors_link

    if related_authors_link == '':
        logging.error('Error in finding related author link')
        return related_authors, related_authors_urls

    try:
        related_authors_html = urlopen(related_authors_link)
    except:
        logging.error('Cannot open related authors link')
        return related_authors, related_authors_urls

    new_soup = BeautifulSoup(related_authors_html, 'html.parser')
    related_author_info_holders = new_soup.find_all('a',
                                                    class_='gr-h3 gr-h3--serif gr-h3--noMargin')
    for related_author_info_holder in related_author_info_holders:
        related_author_name_holder = related_author_info_holder.find(itemprop='name')
        related_authors.append(related_author_name_holder.text.strip())
        related_author_url = related_author_info_holder['href']
        related_authors_urls.append(related_author_url)
    return related_authors[1:], related_authors_urls[1:]


def find_author_books(soup):
    """
    Find the books from the author
    """
    author_books = []
    author_books_holders = soup.find('table', class_='stacked tableList')\
        .find_all('a', class_='bookTitle')
    for author_books_holder in author_books_holders:
        author_books_name_holder = author_books_holder.find(itemprop='name')
        if author_books_name_holder is None:
            continue
        author_books.append(author_books_name_holder.text.strip())
    return author_books


def is_author(url):
    """
    Check whether url is an author page in GoodReads
    """
    if url[:38] != 'https://www.goodreads.com/author/show/':
        return False
    soup = get_soup(url)
    if soup is None:
        return False
    if soup.find('div', class_='rightContainer').find('h1', class_='authorName'):
        return True
    return False
