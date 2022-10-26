import requests

ENDPOINT = ''

def test_can_create_books_and_get_books():
    # The book should be successfully created
    create_response = create_book('test-isbn-001', 'My Book')
    assert create_response.status_code == 200

    # The book should be retrievable upon creation
    isbn = create_response.json()['book']['isbn']
    get_response = get_book(isbn)
    assert get_response.status_code == 200

def test_can_list_books():
    # Create new test books
    create_response = create_book('test-isbn-002', 'My Book 2')
    assert create_response.status_code == 200

    create_response = create_book('test-isbn-003', 'My Book 3')
    assert create_response.status_code == 200

    # Retrieve all books
    list_response = list_books()
    assert list_response.status_code == 200
    books = list_response.json()['books']
    assert len(books) == 3

def test_can_update_book():
    test_book = {
        'title': 'My Book',
        'isbn': 'test-isbn-001',
        'authors': 'Author 1',
        'languages': [
            'EN'
        ],
        'countries': [
            'PH'
        ],
        'number_of_pages': 10,
        'release_date': '2022-10-26'
    }

    # Check that the book exists
    get_response = get_book(test_book['isbn'])
    assert get_response.status_code == 200

    # Update some attributes for the test
    test_book['authors'] = 'Author 2'
    test_book['title'] = 'My New Book'

    # The update call should be successful
    update_response = update_book(test_book)
    assert update_response.status_code == 200

    # Check that the results of GET is updated
    get_response = get_book(test_book['isbn'])
    assert get_response.status_code == 200
    assert get_response.json()['authors'] == 'Author 2'
    assert get_response.json()['title'] == 'My New Book'

def test_can_delete_book():
    # Check that the book exists
    get_response = get_book('test-isbn-001')
    assert get_response.status_code == 200

    get_response = get_book('test-isbn-002')
    assert get_response.status_code == 200

    get_response = get_book('test-isbn-003')
    assert get_response.status_code == 200

    # Delete the book
    delete_book('test-isbn-001')
    delete_book('test-isbn-002')
    delete_book('test-isbn-003')

    # Getting the book should return 404
    get_response = get_book('test-isbn-001')
    assert get_response.status_code == 404

    # Getting the book should return 404
    get_response = get_book('test-isbn-002')
    assert get_response.status_code == 404

    # Getting the book should return 404
    get_response = get_book('test-isbn-003')
    assert get_response.status_code == 404

def create_book(isbn: str, title: str, book_details: dict = None) -> dict:
    if book_details is None:
        book_details = {
            'authors': 'Author 1',
            'languages': [
                'EN'
            ],
            'countries': [
                'PH'
            ],
            'number_of_pages': 10,
            'release_date': '2022-10-26'
        }

    book_details['isbn'] = isbn
    book_details['title'] = title

    return requests.post(f'{ENDPOINT}/books', json=book_details)

def get_book(isbn: str) -> dict:
    return requests.get(f'{ENDPOINT}/books/{isbn}')

def delete_book(isbn: str) -> dict:
    return requests.delete(f'{ENDPOINT}/books/{isbn}')

def update_book(book_details: dict) -> dict:
    return requests.put(f'{ENDPOINT}/books', json=book_details)

def list_books() -> dict:
    return requests.get(f'{ENDPOINT}/books')
