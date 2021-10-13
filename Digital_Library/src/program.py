"""
This module is used to accept user input. It can control the number of
books and authors to scrape. It will use book_scraper and author_scraper
to get the information and then store them into database. It can accept a
JSON file to update or insert into existing database. It can export
existing books/authors to a JSON file. It can perform api functions locally.
"""
import sys

from src.book_scraper import scrape_book_page, is_book
from src.author_scraper import scrape_author_page
from src.database import Database
from src.library_app import get_book_by_id, get_author_by_id, get_by_query, put_book_by_id, \
    put_author_by_id, post_book, post_books, post_author, post_authors, post_scrape, \
    delete_book_by_id, delete_author_by_id

BOOK_WARNING_NUMBER = 200
AUTHOR_WARNING_NUMBER = 50
MAX_STOP_NUMBER = 2000
DASH_NUMBER = 20
OPTION_EXIT = 0
OPTION_ONE = 1
OPTION_TWO = 2
OPTION_THREE = 3
OPTION_FOUR = 4
OPTION_FIVE = 5
OPTION_SIX = 6


def show_menu():
    """
    Show the tree-like menu and read user option
    """
    # Read user input using command line
    while True:
        choice = input("Choose int value from one of the following:\n"
                       "1 = Scrape books and authors by starting url\n"
                       "2 = Read from JSON file and update/insert to database\n"
                       "3 = Simulate web api in command line\n"
                       "4 = Export existing books/authors into src/library.json\n"
                       "0 = EXIT\n\n")
        if not choice.isnumeric():
            continue
        choice = int(choice)
        if OPTION_EXIT <= choice <= OPTION_FOUR:
            break

    # Handle different options
    if choice == OPTION_EXIT:
        sys.exit(0)
    if choice == OPTION_ONE:
        # Scrape web page
        # Get the parameters
        starting_url = input("Please enter the starting url of a book page:\n\n")
        while True:
            number_books = input("Please enter the number of books to scrape:\n\n")
            if not number_books.isnumeric():
                continue
            number_books = int(number_books)
            break
        while True:
            number_authors = input("Please enter the number of authors to scrape:\n\n")
            if not number_authors.isnumeric():
                continue
            number_authors = int(number_authors)
            break
        # Check validity of url
        if not is_book(starting_url):
            # Starting url is not a book page, then print message
            print('Starting url is not a book page')
        else:
            books_url_queue.append(starting_url)
            # Begin to scrape
            scrape(number_books, number_authors)
    if choice == OPTION_TWO:
        # Read from json file and update database
        json_file = input("Please enter the JSON file to read:\n\n")
        if json_file is not None:
            database.update_insert_from_json_file(json_file)
    if choice == OPTION_THREE:
        # Simulate web api in local
        simulate_api()
    if choice == OPTION_FOUR:
        # Export existing books/authors into JSON files
        database.export_to_json_file()


def scrape(number_books, number_authors):
    """
    Scrape from starting url with given number of books and authors.
    Force to stop when count of books/authors in database is 2000.
    Export existing books/authors into JSON files in the end.
    """
    # Print warnings
    if number_books > BOOK_WARNING_NUMBER:
        print('Number of books is greater than 200')
    if number_authors > AUTHOR_WARNING_NUMBER:
        print('Number of authors is greater than 50')

    # Scrape books/authors until the given number
    while len(books_url_set) < number_books or len(authors_url_set) < number_authors:
        if books_tb.count_documents({}) >= MAX_STOP_NUMBER \
                or authors_tb.count_documents({}) >= MAX_STOP_NUMBER:
            print('Program will not go beyond 2000 books or authors')
            break
        # if no book urls and no author urls left in queue to scrape, break the loop
        if len(books_url_queue) == 0 and len(authors_url_queue) == 0:
            break

        # Get current book url to scrape
        while True:
            book_url = books_url_queue.pop(0)
            if len(books_url_queue) == 0 or (book_url not in books_url_set and book_url):
                break
        # Try to scrape current book
        if len(books_url_set) < number_books and book_url not in books_url_set:
            scrape_book_and_store(book_url, number_books)

        # Get current author url to scrape
        while True:
            author_url = authors_url_queue.pop(0)
            if len(authors_url_queue) == 0 or (author_url not in authors_url_set and author_url):
                break
        # Try to scrape current author
        if len(authors_url_set) < number_authors and author_url not in authors_url_set:
            scrape_author_and_store(author_url, number_authors)


def scrape_book_and_store(book_url, number_books):
    """
    Scrape current book and store into database.
    Store the potential books' urls into the queue for future scrape.
    """
    print('-' * DASH_NUMBER, f'Scraping book url {len(books_url_set) + 1}/{number_books}',
          '-' * DASH_NUMBER)
    book_dic, similar_books_urls = scrape_book_page(book_url)
    if book_dic is None:
        return
    database.update_insert_books_tb(book_dic)
    authors_url_queue.append(book_dic['author_url'])
    books_url_set.add(book_dic['book_url'])
    for similar_book_url in similar_books_urls:
        if similar_book_url not in books_url_queue:
            books_url_queue.append(similar_book_url)


def scrape_author_and_store(author_url, number_authors):
    """
    Scrape current author and store into database.
    Store the potential authors' urls into the queue for future scrape.
    """
    print('-' * DASH_NUMBER, f'Scraping author url {len(authors_url_set) + 1}/{number_authors}',
          '-' * DASH_NUMBER)
    author_dic, related_authors_urls = scrape_author_page(author_url)
    if author_dic is None:
        return
    database.update_insert_authors_tb(author_dic)
    authors_url_set.add(author_dic['author_url'])
    for related_author_url in related_authors_urls:
        if related_author_url not in authors_url_queue:
            authors_url_queue.append(related_author_url)


def simulate_api():
    """
    Simulate web api in local.
    Show the menu and read user option, then go to the specified method.
    """
    while True:
        method = input("Choose method of api from one of the following:\n"
                       "1 = GET\n"
                       "2 = PUT\n"
                       "3 = POST\n"
                       "4 = DELETE\n"
                       "5 = go back to previous menu\n\n")
        if not method.isnumeric():
            continue
        method = int(method)
        if OPTION_ONE <= method <= OPTION_FIVE:
            break
    if method == OPTION_ONE:
        get_api()
    if method == OPTION_TWO:
        put_api()
    if method == OPTION_THREE:
        post_api()
    if method == OPTION_FOUR:
        delete_api()
    if method == OPTION_FIVE:
        show_menu()


def get_api():
    """
    Perform api for GET locally
    """
    while True:
        option = input("Choose GET api from one of the following:\n"
                       "1 = api/book?id={attr_value}\n"
                       "2 = api/author?id={attr_value}\n"
                       "3 = api/search?q={query_string}\n"
                       "4 = go back to previous menu\n\n")
        if not option.isnumeric():
            continue
        option = int(option)
        if OPTION_ONE <= option <= OPTION_FOUR:
            break
    if option == OPTION_ONE:
        value = input("api/book?id=")
        print(get_book_by_id(value))
    if option == OPTION_TWO:
        value = input("api/author?id=")
        print(get_author_by_id(value))
    if option == OPTION_THREE:
        value = input("api/search?q=")
        print(get_by_query(value))
    if option == OPTION_FOUR:
        simulate_api()


def put_api():
    """
    Perform api for PUT locally
    """
    while True:
        option = input("Choose PUT api from one of the following:\n"
                       "1 = api/book?id={attr_value}\n"
                       "2 = api/author?id={attr_value}\n"
                       "3 = go back to previous menu\n\n")
        if not option.isnumeric():
            continue
        option = int(option)
        if OPTION_ONE <= option <= OPTION_THREE:
            break
    if option == OPTION_ONE:
        value = input("api/book?id=")
        file = input("json file: ")
        print(put_book_by_id(value, file))
    if option == OPTION_TWO:
        value = input("api/author?id=")
        file = input("json file: ")
        print(put_author_by_id(value, file))
    if option == OPTION_THREE:
        simulate_api()


def post_api():
    """
    Perform api for POST locally
    """
    while True:
        option = input("Choose POST api from one of the following:\n"
                       "1 = api/book\n"
                       "2 = api/books\n"
                       "3 = api/author\n"
                       "4 = api/authors\n"
                       "5 = api/scrape?attr={attr_value}\n"
                       "6 = go back to previous menu\n\n")
        if not option.isnumeric():
            continue
        option = int(option)
        if OPTION_ONE <= option <= OPTION_SIX:
            break
    if option == OPTION_ONE:
        file = input("json file: ")
        print(post_book(file))
    if option == OPTION_TWO:
        file = input("json file: ")
        print(post_books(file))
    if option == OPTION_THREE:
        file = input("json file: ")
        print(post_author(file))
    if option == OPTION_FOUR:
        file = input("json file: ")
        print(post_authors(file))
    if option == OPTION_FIVE:
        value = input("api/scrape?attr=")
        print(post_scrape(value))
    if option == OPTION_SIX:
        simulate_api()


def delete_api():
    """
    Perform api for DELETE locally
    """
    while True:
        option = input("Choose DELETE api from one of the following:\n"
                       "1 = api/book?id={attr_value}\n"
                       "2 = api/author?id={attr_value}\n"
                       "3 = go back to previous menu\n\n")
        if not option.isnumeric():
            continue
        option = int(option)
        if OPTION_ONE <= option <= OPTION_THREE:
            break
    if option == OPTION_ONE:
        value = input("api/book?id=")
        print(delete_book_by_id(value))
    if option == OPTION_TWO:
        value = input("api/author?id=")
        print(delete_author_by_id(value))
    if option == OPTION_THREE:
        simulate_api()


if __name__ == '__main__':
    # Initialize database
    database = Database()
    books_tb = database.books_tb
    authors_tb = database.authors_tb
    # Initialize required containers
    books_url_set = set()
    authors_url_set = set()
    books_url_queue = []
    authors_url_queue = []
    # Show the tree-like menu in terminal
    show_menu()
