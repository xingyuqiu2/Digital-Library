# Digital Library

## Description
Backend:\
Gather information of Authors and Books from Goodreads. Report progress and exceptions.\
Represent book with attributes {'book_url', 'title', 'book_id', 'ISBN', 'author_url', 'author', 'rating', 'rating_count', 'review_count', 'image_url', 'similar_books'}.\
Represent author with attributes {'name', 'author_url', 'author_id', 'rating', 'rating_count', 'review_count', 'image_url', 'related_authors', 'author_books'}\
Store data into the database while scraping. Accept any valid starting URL. Accept an arbitrary number of books and authors to scrape.\
Read from JSON files to create new books/authors or update existing books/authors.\
Export existing books/authors into JSON files.\
Perform web api functions or simulate api locally.

For the search function in GET api, program supports the following query string (without nested operations):\
. operator to specify a field of an object. For example, book.rating_count\
: operator to specify if a field contains search words. For example, book.book_id:123\
"" operators to specify the exact search term. For example, book.image_url:"123"\
AND, OR, and NOT logical operators. For example, book.rating_count: NOT 123\
One-side unbounded comparison operators >, <. For example, book.rating_count: > 123

Frontend:\
Use form-like structure that allows users to type values in each field.\
Making CRUD requests to the server via JavaScript.\
Render the content of result from CRUD requests via JavaScript.\
Notifying users of success PUT, POST, and DELETE, and also notifying users of errors that occurred.\
Responsive design that supports both mobile devices and desktop.\
visualizations of ranking of the top k highest-rated books/authors on the webpage using d3.js and svg elements.\


## Folders and files in Project
- src/
    - static/
        - css/
            - index.css
            - get_or_delete.css
            - put_or_post.css
            - top_books_authors.css
        - js/
            - index.js
            - get_or_delete.js
            - put_or_post.js
            - top_books.js
            - top_authors.js
    - templates/
        - index.html
        - get_or_delete.html
        - put_or_post.html
        - top_books.html
        - top_authors.html
    - test/
        - test_book_scraper.py
        - test_author_scraper.py
        - test_database.py
        - test_api.py
    - book_scraper.py
    - author_scraper.py
    - database.py
    - library_app.py
    - query.py
    - program.py

## Usage
Create a .env file and store the HOST and PORT of mongoDB\
e.g.\
HOST='localhost'\
PORT=27017

Download flask with virtual environment under Digital_Library directory, then run: venv/Scripts/activate

1. Under Digital_Library directory, run in terminal: py -m src.program\
Then follow the tree-like menu shown in terminal

2. Under Digital_Library directory, run in terminal: py -m src.library_app\
Then open in browser: http://127.0.0.1:5000/