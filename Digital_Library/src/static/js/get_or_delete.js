BOOK_ATTRIBUTES = ['book_id', 'title', 'book_url', 'ISBN', 'author_url', 'author', 'rating',
                   'rating_count', 'review_count', 'image_url', 'similar_books']
AUTHOR_ATTRIBUTES = ['author_id', 'name', 'author_url', 'rating', 'rating_count',
                     'review_count', 'image_url', 'related_authors', 'author_books']

const body = document.body
const header = document.createElement('h1')
header.setAttribute('onclick', 'window.location = "http://127.0.0.1:5000/"')
header.innerText = 'Digital Library'
body.append(header)

const paragraph = document.createElement('p')
paragraph.setAttribute('class', 'paragraph')
body.append(paragraph)


// Create div for get/delete book by id
const bookDiv = document.createElement('div')
paragraph.append(bookDiv)

const bookHeader = document.createElement('h3')
bookHeader.innerText = 'Enter the book id: '
bookDiv.append(bookHeader)
// Book form
const bookForm = document.createElement('form')
bookDiv.append(bookForm)
const bookIdInput = document.createElement('input')
bookIdInput.setAttribute('type', 'text')
bookForm.append(bookIdInput)
// Buttons
const buttonGetBook = document.createElement('button')
buttonGetBook.setAttribute('class', 'button-get-book')
buttonGetBook.innerText = 'search'
bookForm.append(buttonGetBook)
const buttonDeleteBook = document.createElement('button')
buttonDeleteBook.setAttribute('class', 'button-delete-book')
buttonDeleteBook.innerText = 'delete'
bookForm.append(buttonDeleteBook)


// Create div for get/delete author by id
const authorDiv = document.createElement('div')
paragraph.append(authorDiv)

const authorHeader = document.createElement('h3')
authorHeader.innerText = 'Enter the author id: '
authorDiv.append(authorHeader)
// Author form
const authorForm = document.createElement('form')
authorDiv.append(authorForm)
const authorIdInput = document.createElement('input')
authorIdInput.setAttribute('type', 'text')
authorForm.append(authorIdInput)
// Buttons
const buttonGetAuthor = document.createElement('button')
buttonGetAuthor.setAttribute('class', 'button-get-author')
buttonGetAuthor.innerText = 'search'
authorForm.append(buttonGetAuthor)
const buttonDeleteAuthor = document.createElement('button')
buttonDeleteAuthor.setAttribute('class', 'button-delete-author')
buttonDeleteAuthor.innerText = 'delete'
authorForm.append(buttonDeleteAuthor)


// Create div for search
const searchDiv = document.createElement('div')
paragraph.append(searchDiv)
const searchHeader = document.createElement('h3')
searchHeader.innerText = 'Choose the object and field for search, then enter the content'
searchDiv.append(searchHeader)

// Create div for search single book
const bookSearchDiv = document.createElement('div')
bookSearchDiv.setAttribute('class', 'book-search-div')
bookSearchDiv.innerText = 'book '
searchDiv.append(bookSearchDiv)
// Select first field
const bookFieldSelector = document.createElement('select')
bookFieldSelector.setAttribute('class', 'book-field-selector')
bookFieldSelector.setAttribute('name', 'book-field')
for (var i = 0; i < BOOK_ATTRIBUTES.length; i++) {
    const option = document.createElement('option')
    option.innerText = BOOK_ATTRIBUTES[i]
    bookFieldSelector.append(option)
}
bookSearchDiv.append(bookFieldSelector)
// Enter first content
const bookContentForm = document.createElement('form')
bookContentForm.setAttribute('class', 'book-content-form')
bookContentForm.innerText = 'Content: '
const bookContentInput = document.createElement('input')
bookContentInput.setAttribute('type', 'text')
const bookFirstSearchButton = document.createElement('button')
bookFirstSearchButton.setAttribute('id', 'single-book-search-button')
bookFirstSearchButton.innerText = 'search'
bookContentForm.append(bookContentInput)
bookContentForm.append(bookFirstSearchButton)
bookSearchDiv.append(bookContentForm)

// Create div for search book with logical operator
const bookSearchLogicalDiv = document.createElement('div')
bookSearchLogicalDiv.setAttribute('class', 'book-search-logical-div')
searchDiv.append(bookSearchLogicalDiv)

// Create selector for AND/OR
const bookLogicalSelector = document.createElement('select')
bookLogicalSelector.setAttribute('class', 'book-logical-selector')
bookLogicalSelector.setAttribute('name', 'book-logical-operator')
const optionAnd = document.createElement('option')
optionAnd.innerText = 'AND'
bookLogicalSelector.append(optionAnd)
const optionOr = document.createElement('option')
optionOr.innerText = 'OR'
bookLogicalSelector.append(optionOr)
bookSearchLogicalDiv.append(bookLogicalSelector)
// Select second field
const bookSecondFieldSelector = document.createElement('select')
bookSecondFieldSelector.setAttribute('class', 'book-second-field-selector')
bookSecondFieldSelector.setAttribute('name', 'book-second-field')
for (var i = 0; i < BOOK_ATTRIBUTES.length; i++) {
    const option = document.createElement('option')
    option.innerText = BOOK_ATTRIBUTES[i]
    bookSecondFieldSelector.append(option)
}
bookSearchLogicalDiv.append(bookSecondFieldSelector)
// Enter second content
const bookSecondContentForm = document.createElement('form')
bookSecondContentForm.setAttribute('class', 'book-second-content-form')
bookSecondContentForm.innerText = 'Content: '
const bookSecondContentInput = document.createElement('input')
bookSecondContentInput.setAttribute('type', 'text')
const bookSecondSearchButton = document.createElement('button')
bookSecondSearchButton.setAttribute('id', 'double-book-search-button')
bookSecondSearchButton.innerText = 'search'
bookSecondContentForm.append(bookSecondContentInput)
bookSecondContentForm.append(bookSecondSearchButton)
bookSearchLogicalDiv.append(bookSecondContentForm)


// Create div for search author
const authorSearchDiv = document.createElement('div')
authorSearchDiv.setAttribute('class', 'author-search-div')
authorSearchDiv.innerText = 'author'
searchDiv.append(authorSearchDiv)
// Select first field
const authorFieldSelector = document.createElement('select')
authorFieldSelector.setAttribute('class', 'author-field-selector')
authorFieldSelector.setAttribute('name', 'author-field')
for (var i = 0; i < AUTHOR_ATTRIBUTES.length; i++) {
    const option = document.createElement('option')
    option.innerText = AUTHOR_ATTRIBUTES[i]
    authorFieldSelector.append(option)
}
authorSearchDiv.append(authorFieldSelector)
// Enter first content
const authorContentForm = document.createElement('form')
authorContentForm.setAttribute('class', 'author-content-form')
authorContentForm.innerText = 'Content: '
const authorContentInput = document.createElement('input')
authorContentInput.setAttribute('type', 'text')
const authorFirstSearchButton = document.createElement('button')
authorFirstSearchButton.setAttribute('id', 'single-author-search-button')
authorFirstSearchButton.innerText = 'search'
authorContentForm.append(authorContentInput)
authorContentForm.append(authorFirstSearchButton)
authorSearchDiv.append(authorContentForm)

// Create div for search author with logical operator
const authorSearchLogicalDiv = document.createElement('div')
authorSearchLogicalDiv.setAttribute('class', 'author-search-logical-div')
searchDiv.append(authorSearchLogicalDiv)

// Create selector for AND/OR
const authorLogicalSelector = document.createElement('select')
authorLogicalSelector.setAttribute('class', 'author-logical-selector')
authorLogicalSelector.setAttribute('name', 'author-logical-operator')
const optionAuthorAnd = document.createElement('option')
optionAuthorAnd.innerText = 'AND'
authorLogicalSelector.append(optionAuthorAnd)
const optionAuthorOr = document.createElement('option')
optionAuthorOr.innerText = 'OR'
authorLogicalSelector.append(optionAuthorOr)
authorSearchLogicalDiv.append(authorLogicalSelector)
// Select second field
const authorSecondFieldSelector = document.createElement('select')
authorSecondFieldSelector.setAttribute('class', 'author-second-field-selector')
authorSecondFieldSelector.setAttribute('name', 'author-second-field')
for (var i = 0; i < AUTHOR_ATTRIBUTES.length; i++) {
    const option = document.createElement('option')
    option.innerText = AUTHOR_ATTRIBUTES[i]
    authorSecondFieldSelector.append(option)
}
authorSearchLogicalDiv.append(authorSecondFieldSelector)
// Enter second content
const authorSecondContentForm = document.createElement('form')
authorSecondContentForm.setAttribute('class', 'author-second-content-form')
authorSecondContentForm.innerText = 'Content: '
const authorSecondContentInput = document.createElement('input')
authorSecondContentInput.setAttribute('type', 'text')
const authorSecondSearchButton = document.createElement('button')
authorSecondSearchButton.setAttribute('id', 'double-author-search-button')
authorSecondSearchButton.innerText = 'search'
authorSecondContentForm.append(authorSecondContentInput)
authorSecondContentForm.append(authorSecondSearchButton)
authorSearchLogicalDiv.append(authorSecondContentForm)

// Create list
const list = document.createElement('ul')
list.setAttribute('id', 'list')
paragraph.append(list)


/**
 * Function to fetch books/authors data using web api.
 * Then render the results in list.
 * Called by get or delete method.
 * @param {String} relUrl relative url for api
 * @param {String} title used to indicate object type, book or author
 * @param {String} meth CRUD request, either GET or DELETE
 */
async function getOrDeleteObjectById(relUrl, title, meth) {
    fetch('http://127.0.0.1:5000/api/' + relUrl, {
        method: meth
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

/**
 * Function to fetch books/authors data using web api.
 * Then render the results in list.
 * Called by get by search method.
 * @param {String} attr relative url for api
 * @param {String} title used to indicate object type, books or authors
 */
async function getBySearch(attr, title) {
    fetch('http://127.0.0.1:5000/api/search?q=' + attr, {
        method: 'GET'
    })
    .then(response => {
        return response.json()
    })
    .then(data => {
        console.log(data)
        const objLi = document.createElement('li')
        objLi.innerText = title
        list.append(objLi)
        if (data instanceof Array !== true) {
            const li = document.createElement('li')
            for (var key in data) {
                li.innerHTML += '[' + key + '] ' + data[key] + '</br>'
            }
            list.append(li)
        } else {
            for (var i = 0; i < data.length; i++) {
                var doc = data[i]
                const li = document.createElement('li')
                for (var key in doc) {
                    li.innerHTML += '[' + key + '] ' + doc[key] + '</br>'
                }
                list.append(li)
            }
        }
    })
    .catch(error => {
        console.log(error)
    })
}

// Add event listener for all the buttons
buttonGetBook.addEventListener(
    'click',
    function(e) {
    e.preventDefault()
    getOrDeleteObjectById('book?id=' + bookIdInput.value, '--BOOK--', 'GET')
})

buttonDeleteBook.addEventListener(
    'click',
    function(e) {
    e.preventDefault()
    getOrDeleteObjectById('book?id=' + bookIdInput.value, '--BOOK--', 'DELETE')
})

buttonGetAuthor.addEventListener(
    'click',
    function(e) {
    e.preventDefault()
    getOrDeleteObjectById('author?id=' + authorIdInput.value, '--AUTHOR--', 'GET')
})

buttonDeleteAuthor.addEventListener(
    'click',
    function(e) {
    e.preventDefault()
    getOrDeleteObjectById('author?id=' + authorIdInput.value, '--AUTHOR--', 'DELETE')
})

bookFirstSearchButton.addEventListener(
    'click',
    function(e) { 
    e.preventDefault()
    var field = bookFieldSelector.options[bookFieldSelector.selectedIndex].text
    var content = bookContentInput.value
    var query = 'book.' + field + ':' + content
    getBySearch(query, '--BOOKS--')
})

bookSecondSearchButton.addEventListener(
    'click',
    function(e) { 
    e.preventDefault()
    var firstField = bookFieldSelector.options[bookFieldSelector.selectedIndex].text
    var firstContent = bookContentInput.value
    var logicalOperator = bookLogicalSelector.options[bookLogicalSelector.selectedIndex].text
    var secondField = bookSecondFieldSelector.options[bookSecondFieldSelector.selectedIndex].text
    var secondContent = bookSecondContentInput.value
    var query = 'book.' + firstField + ':' + firstContent + logicalOperator + 'book.' + secondField + ':' + secondContent
    getBySearch(query, '--BOOKS--')
})

authorFirstSearchButton.addEventListener(
    'click',
    function(e) { 
    e.preventDefault()
    var field = authorFieldSelector.options[authorFieldSelector.selectedIndex].text
    var content = authorContentInput.value
    var query = 'author.' + field + ':' + content
    getBySearch(query, '--AUTHORS--')
})

authorSecondSearchButton.addEventListener(
    'click',
    function(e) { 
    e.preventDefault()
    var firstField = authorFieldSelector.options[authorFieldSelector.selectedIndex].text
    var firstContent = authorContentInput.value
    var logicalOperator = authorLogicalSelector.options[authorLogicalSelector.selectedIndex].text
    var secondField = authorSecondFieldSelector.options[authorSecondFieldSelector.selectedIndex].text
    var secondContent = authorSecondContentInput.value
    var query = 'author.' + firstField + ':' + firstContent + logicalOperator + 'author.' + secondField + ':' + secondContent
    getBySearch(query, '--AUTHORS--')
})