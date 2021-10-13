const body = document.body
const header = document.createElement('h1')
header.setAttribute('onclick', 'window.location = "http://127.0.0.1:5000/"')
header.innerText = 'Digital Library'
body.append(header)

const paragraph = document.createElement('p')
paragraph.setAttribute('class', 'paragraph')
body.append(paragraph)

// Create div for put book
const bookDiv = document.createElement('div')
paragraph.append(bookDiv)
const bookHeader = document.createElement('h3')
bookHeader.innerText = 'Enter the book information: '
bookDiv.append(bookHeader)

// Create forms for all book attributes
const bookIdForm = document.createElement('form')
bookDiv.append(bookIdForm)
bookIdForm.innerText = 'book id: '
const bookIdInput = document.createElement('input')
bookIdInput.setAttribute('class', 'book-id-input')
bookIdForm.append(bookIdInput)

const bookTitleForm = document.createElement('form')
bookDiv.append(bookTitleForm)
bookTitleForm.innerText = 'title: '
const bookTitleInput = document.createElement('input')
bookTitleInput.setAttribute('class', 'book-title-input')
bookTitleForm.append(bookTitleInput)

const bookUrlForm = document.createElement('form')
bookDiv.append(bookUrlForm)
bookUrlForm.innerText = 'book url: '
const bookUrlInput = document.createElement('input')
bookUrlInput.setAttribute('class', 'book-url-input')
bookUrlForm.append(bookUrlInput)

const bookIsbnForm = document.createElement('form')
bookDiv.append(bookIsbnForm)
bookIsbnForm.innerText = 'ISBN: '
const bookIsbnInput = document.createElement('input')
bookIsbnInput.setAttribute('class', 'book-isbn-input')
bookIsbnForm.append(bookIsbnInput)

const bookAuthorUrlForm = document.createElement('form')
bookDiv.append(bookAuthorUrlForm)
bookAuthorUrlForm.innerText = 'author url: '
const bookAuthorUrlInput = document.createElement('input')
bookAuthorUrlInput.setAttribute('class', 'book-author-url-input')
bookAuthorUrlForm.append(bookAuthorUrlInput)

const bookAuthorForm = document.createElement('form')
bookDiv.append(bookAuthorForm)
bookAuthorForm.innerText = 'author: '
const bookAuthorInput = document.createElement('input')
bookAuthorInput.setAttribute('class', 'book-author-input')
bookAuthorForm.append(bookAuthorInput)

const bookRatingForm = document.createElement('form')
bookDiv.append(bookRatingForm)
bookRatingForm.innerText = 'rating: '
const bookRatingInput = document.createElement('input')
bookRatingInput.setAttribute('class', 'book-rating-input')
bookRatingForm.append(bookRatingInput)

const bookRatingCountForm = document.createElement('form')
bookDiv.append(bookRatingCountForm)
bookRatingCountForm.innerText = 'rating count: '
const bookRatingCountInput = document.createElement('input')
bookRatingCountInput.setAttribute('class', 'book-rating-count-input')
bookRatingCountForm.append(bookRatingCountInput)

const bookReviewCountForm = document.createElement('form')
bookDiv.append(bookReviewCountForm)
bookReviewCountForm.innerText = 'review count: '
const bookReviewCountInput = document.createElement('input')
bookReviewCountInput.setAttribute('class', 'book-review-count-input')
bookReviewCountForm.append(bookReviewCountInput)

const bookImageUrlForm = document.createElement('form')
bookDiv.append(bookImageUrlForm)
bookImageUrlForm.innerText = 'image url: '
const bookImageUrlInput = document.createElement('input')
bookImageUrlInput.setAttribute('class', 'book-image-url-input')
bookImageUrlForm.append(bookImageUrlInput)

const bookSimilarBooksForm = document.createElement('form')
bookDiv.append(bookSimilarBooksForm)
bookSimilarBooksForm.innerText = 'similar books: '
const bookSimilarBooksInput = document.createElement('input')
bookSimilarBooksInput.setAttribute('class', 'book-similar-books-input')
bookSimilarBooksForm.append(bookSimilarBooksInput)

// Create buttons for append and put
const bookButtonsDiv = document.createElement('div')
bookButtonsDiv.setAttribute('class', 'book-buttons-div')
paragraph.append(bookButtonsDiv)

const buttonPutOneBook = document.createElement('button')
buttonPutOneBook.setAttribute('class', 'button-put-one-book')
buttonPutOneBook.innerText = 'Put One'
bookButtonsDiv.append(buttonPutOneBook)
const buttonPostOneBook = document.createElement('button')
buttonPostOneBook.setAttribute('class', 'button-post-one-book')
buttonPostOneBook.innerText = 'Post One'
bookButtonsDiv.append(buttonPostOneBook)
const buttonAppendBook = document.createElement('button')
buttonAppendBook.setAttribute('class', 'button-append-book')
buttonAppendBook.innerText = 'Append'
bookButtonsDiv.append(buttonAppendBook)
const buttonPostAllBook = document.createElement('button')
buttonPostAllBook.setAttribute('class', 'button-post-all-book')
buttonPostAllBook.innerText = 'Post All'
bookButtonsDiv.append(buttonPostAllBook)


// Create div for put author
const authorDiv = document.createElement('div')
paragraph.append(authorDiv)
const authorHeader = document.createElement('h3')
authorHeader.innerText = 'Enter the author information: '
authorDiv.append(authorHeader)

// Create forms for all author attributes
const authorIdForm = document.createElement('form')
authorDiv.append(authorIdForm)
authorIdForm.innerText = 'author id: '
const authorIdInput = document.createElement('input')
authorIdInput.setAttribute('class', 'author-id-input')
authorIdForm.append(authorIdInput)

const authorNameForm = document.createElement('form')
authorDiv.append(authorNameForm)
authorNameForm.innerText = 'name: '
const authorNameInput = document.createElement('input')
authorNameInput.setAttribute('class', 'author-name-input')
authorNameForm.append(authorNameInput)

const authorUrlForm = document.createElement('form')
authorDiv.append(authorUrlForm)
authorUrlForm.innerText = 'author url: '
const authorUrlInput = document.createElement('input')
authorUrlInput.setAttribute('class', 'author-url-input')
authorUrlForm.append(authorUrlInput)

const authorRatingForm = document.createElement('form')
authorDiv.append(authorRatingForm)
authorRatingForm.innerText = 'rating: '
const authorRatingInput = document.createElement('input')
authorRatingInput.setAttribute('class', 'author-rating-input')
authorRatingForm.append(authorRatingInput)

const authorRatingCountForm = document.createElement('form')
authorDiv.append(authorRatingCountForm)
authorRatingCountForm.innerText = 'rating count: '
const authorRatingCountInput = document.createElement('input')
authorRatingCountInput.setAttribute('class', 'author-rating-count-input')
authorRatingCountForm.append(authorRatingCountInput)

const authorReviewCountForm = document.createElement('form')
authorDiv.append(authorReviewCountForm)
authorReviewCountForm.innerText = 'review count: '
const authorReviewCountInput = document.createElement('input')
authorReviewCountInput.setAttribute('class', 'author-review-count-input')
authorReviewCountForm.append(authorReviewCountInput)

const authorImageUrlForm = document.createElement('form')
authorDiv.append(authorImageUrlForm)
authorImageUrlForm.innerText = 'image url: '
const authorImageUrlInput = document.createElement('input')
authorImageUrlInput.setAttribute('class', 'author-image-url-input')
authorImageUrlForm.append(authorImageUrlInput)

const authorRelatedAuthorsForm = document.createElement('form')
authorDiv.append(authorRelatedAuthorsForm)
authorRelatedAuthorsForm.innerText = 'related authors: '
const authorRelatedAuthorsInput = document.createElement('input')
authorRelatedAuthorsInput.setAttribute('class', 'author-related-authors-input')
authorRelatedAuthorsForm.append(authorRelatedAuthorsInput)

const authorBooksForm = document.createElement('form')
authorDiv.append(authorBooksForm)
authorBooksForm.innerText = 'author books: '
const authorBooksInput = document.createElement('input')
authorBooksInput.setAttribute('class', 'author-books-input')
authorBooksForm.append(authorBooksInput)

// Create buttons for append and put
const authorButtonsDiv = document.createElement('div')
authorButtonsDiv.setAttribute('class', 'author-buttons-div')
paragraph.append(authorButtonsDiv)

const buttonPutOneAuthor = document.createElement('button')
buttonPutOneAuthor.setAttribute('class', 'button-put-one-author')
buttonPutOneAuthor.innerText = 'Put One'
authorButtonsDiv.append(buttonPutOneAuthor)
const buttonPostOneAuthor = document.createElement('button')
buttonPostOneAuthor.setAttribute('class', 'button-post-one-author')
buttonPostOneAuthor.innerText = 'Post One'
authorButtonsDiv.append(buttonPostOneAuthor)
const buttonAppendAuthor = document.createElement('button')
buttonAppendAuthor.setAttribute('class', 'button-append-author')
buttonAppendAuthor.innerText = 'Append'
authorButtonsDiv.append(buttonAppendAuthor)
const buttonPostAllAuthor = document.createElement('button')
buttonPostAllAuthor.setAttribute('class', 'button-post-all-author')
buttonPostAllAuthor.innerText = 'Post All'
authorButtonsDiv.append(buttonPostAllAuthor)


// Create div for scrape
const scrapeDiv = document.createElement('div')
paragraph.append(scrapeDiv)
const scrapeHeader = document.createElement('h3')
scrapeHeader.innerText = 'Enter the url of book/author to scrape: '
scrapeDiv.append(scrapeHeader)

// Create forms for scrape
const scrapeForm = document.createElement('form')
scrapeDiv.append(scrapeForm)
scrapeForm.innerText = 'url to scrape: '
const scrapeInput = document.createElement('input')
scrapeInput.setAttribute('class', 'scrape-input')
scrapeForm.append(scrapeInput)
const scrapeButtonDiv = document.createElement('div')
scrapeDiv.append(scrapeButtonDiv)
const scrapeButton = document.createElement('button')
scrapeButton.innerText = 'Scrape'
scrapeButtonDiv.append(scrapeButton)


// Create list
const list = document.createElement('ul')
list.setAttribute('id', 'list')
paragraph.append(list)


// List of books/authors to post
var listBooksToPost = []
var listAuthorsToPost = []


/**
 * Combine the values from input boxes to form book dictionary.
 * @param {String} meth CRUD request method, PUT or POST
 * @returns book dictionary
 */
function computeBookDict(meth) {
    var bookId = bookIdInput.value
    var title = bookTitleInput.value
    var bookUrl = bookUrlInput.value
    var isbn = bookIsbnInput.value
    var authorUrl = authorUrlInput.value
    var author = bookAuthorInput.value
    var rating = bookRatingInput.value
    var ratingCount = bookRatingCountInput.value
    var reviewCount = bookReviewCountInput.value
    var imageUrl = bookImageUrlInput.value
    var similarBooks = bookSimilarBooksInput.value
    var dict = {'book_id': bookId, 'title': title, 'book_url': bookUrl, 'ISBN': isbn, 'author_url': authorUrl, 'author': author, 
    'rating': rating, 'rating_count': ratingCount, 'review_count': reviewCount, 'image_url': imageUrl, 'similar_books': similarBooks}
    if (meth === "PUT") {
        delete dict['book_id']
    }
    return dict
}

/**
 * Combine the values from input boxes to form author dictionary.
 * @param {String} meth CRUD request method, PUT or POST
 * @returns author dictionary
 */
function computeAuthorDict(meth) {
    var authorId = authorIdInput.value
    var name = authorNameInput.value
    var authorUrl = authorUrlInput.value
    var rating = authorRatingInput.value
    var ratingCount = authorRatingCountInput.value
    var reviewCount = authorReviewCountInput.value
    var imageUrl = authorImageUrlInput.value
    var relatedAuthors = authorRelatedAuthorsInput.value
    var authorBooks = authorBooksInput.value
    var dict = {'author_id': authorId, 'name': name, 'author_url': authorUrl, 'rating': rating, 'rating_count': ratingCount, 
               'review_count': reviewCount, 'image_url': imageUrl, 'related_authors': relatedAuthors, 'author_books': authorBooks}
    if (meth === "PUT") {
        delete dict['author_id']
    }
    return dict
}

/**
 * Function to fetch books/authors data using web api.
 * Then render the results in list.
 * Called by put or post method.
 * @param {String} relUrl relative url for api
 * @param {String} title used to indicate object type, book or author
 * @param {String} meth CRUD request, either PUT or POST
 * @param {json} data json data converted from dictionary or list of dictionary
 */
async function putOrPostObject(relUrl, title, meth, data) {
    fetch('http://127.0.0.1:5000/api/' + relUrl, {
        method: meth,
        headers: {
            'Content-Type': 'application/json'
        },
        body: data
    })
    .then(response => {
        return response.json()
    })
    .then(data => {
        console.log(data)
        const objLi = document.createElement('li')
        objLi.innerText = title
        list.append(objLi)
        const li = document.createElement('li')
        for (var key in data) {
            li.innerHTML += '[' + key + '] ' + data[key] + '</br>'
        }
        list.append(li)
    })
    .catch(error => {
        console.log(error)
    })
}

// Add event listeners to buttons
buttonPutOneBook.addEventListener(
    'click',
    function(e) { 
    e.preventDefault()
    var meth = 'PUT'
    dict = computeBookDict(meth)
    relUrl = 'book?id=' + bookIdInput.value
    putOrPostObject(relUrl, '--BOOK--', meth, JSON.stringify(dict))
})

buttonPostOneBook.addEventListener(
    'click',
    function(e) { 
    e.preventDefault()
    var meth = 'POST'
    dict = computeBookDict(meth)
    relUrl = 'book'
    putOrPostObject(relUrl, '--BOOK--', meth, JSON.stringify(dict))
})

buttonAppendBook.addEventListener(
    'click',
    function(e) { 
    e.preventDefault()
    var meth = 'POST'
    dict = computeBookDict(meth)
    listBooksToPost.push(dict)
    const li = document.createElement('li')
    li.innerText += 'There are ' + listBooksToPost.length + ' books in pending book list'
    list.append(li)
})

buttonPostAllBook.addEventListener(
    'click',
    function(e) { 
    e.preventDefault()
    var meth = 'POST'
    relUrl = 'books'
    putOrPostObject(relUrl, '--BOOKS--', meth, JSON.stringify(listBooksToPost))
    listBooksToPost = []
})

buttonPutOneAuthor.addEventListener(
    'click',
    function(e) { 
    e.preventDefault()
    var meth = 'PUT'
    dict = computeAuthorDict(meth)
    relUrl = 'author?id=' + authorIdInput.value
    putOrPostObject(relUrl, '--AUTHOR--', meth, JSON.stringify(dict))
})

buttonPostOneAuthor.addEventListener(
    'click',
    function(e) { 
    e.preventDefault()
    var meth = 'POST'
    dict = computeAuthorDict(meth)
    relUrl = 'author'
    putOrPostObject(relUrl, '--AUTHOR--', meth, JSON.stringify(dict))
})

buttonAppendAuthor.addEventListener(
    'click',
    function(e) { 
    e.preventDefault()
    var meth = 'POST'
    dict = computeAuthorDict(meth)
    listAuthorsToPost.push(dict)
    const li = document.createElement('li')
    li.innerText += 'There are ' + listAuthorsToPost.length + ' authors in pending author list'
    list.append(li)
})

buttonPostAllAuthor.addEventListener(
    'click',
    function(e) { 
    e.preventDefault()
    var meth = 'POST'
    relUrl = 'authors'
    putOrPostObject(relUrl, '--AUTHORS--', meth, JSON.stringify(listAuthorsToPost))
    listAuthorsToPost = []
})

scrapeButton.addEventListener(
    'click',
    function(e) { 
    e.preventDefault()
    var meth = 'POST'
    relUrl = 'scrape?attr=' + scrapeInput.value
    putOrPostObject(relUrl, '--SCRAPE--', meth, null)
})