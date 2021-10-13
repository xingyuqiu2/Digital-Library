const body = document.body
const header = document.createElement('h1')
header.innerText = 'Choose An Option'
body.append(header)

const paragraph = document.createElement('p')
body.append(paragraph)

// Create button for CRUD requests GET and DELETE
const buttonGetOrDelete = document.createElement('button')
buttonGetOrDelete.setAttribute('id', 'button-get-or-delete')
buttonGetOrDelete.innerText = 'GET or DELETE'
buttonGetOrDelete.setAttribute('onclick', 'window.location = "http://127.0.0.1:5000/get_or_delete"')
paragraph.append(buttonGetOrDelete)

// Create button for CRUD requests PUT and POST
const buttonPutOrPost = document.createElement('button')
buttonPutOrPost.setAttribute('id', 'button-put-or-post')
buttonPutOrPost.innerText = 'PUT or POST'
buttonPutOrPost.setAttribute('onclick', 'window.location = "http://127.0.0.1:5000/put_or_post"')
paragraph.append(buttonPutOrPost)

// Create button for top books visualization
const buttonTopBooks = document.createElement('button')
buttonTopBooks.setAttribute('id', 'button-top-books')
buttonTopBooks.innerText = 'Get Top Books'
buttonTopBooks.setAttribute('onclick', 'window.location = "http://127.0.0.1:5000/vis/top-books"')
paragraph.append(buttonTopBooks)

// Create button for top authors visualization
const buttonTopAuthors = document.createElement('button')
buttonTopAuthors.setAttribute('id', 'button-top-authors')
buttonTopAuthors.innerText = 'Get Top Authors'
buttonTopAuthors.setAttribute('onclick', 'window.location = "http://127.0.0.1:5000/vis/top-authors"')
paragraph.append(buttonTopAuthors)
