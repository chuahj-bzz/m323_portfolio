from flask import Blueprint, jsonify, request
from book_dao import BookDao
from book import Book

# Book Blueprint
book_blueprint = Blueprint('book_blueprint', __name__)
dao = BookDao('library.db')


@book_blueprint.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(None, data['title'], data['author'], data['genre'], data['is_read'])
    dao.add_book(new_book)
    return jsonify({'message': 'Book added successfully'}), 201


@book_blueprint.route('/books', methods=['GET'])
def get_all_books():
    books = dao.get_all_books()
    if books:
        return jsonify([book.__dict__ for book in books]), 200
    else:
        return jsonify({'message': 'No books found'}), 404


@book_blueprint.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    selected_book = dao.get_book_by_id(book_id)
    if selected_book:
        return jsonify(selected_book.__dict__), 200
    else:
        return jsonify({'message': 'Book not found'}), 404


@book_blueprint.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    updated_book = Book(book_id, data['title'], data['author'], data['genre'], data['is_read'])
    if dao.update_book(updated_book):
        return jsonify({'message': 'Book updated successfully'}), 200
    else:
        return jsonify({'message': 'Book not found or not updated'}), 404


@book_blueprint.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    if dao.delete_book(book_id):
        return jsonify({'message': 'Book deleted successfully'}), 200
    else:
        return jsonify({'message': 'Book not found or not deleted'}), 404


@book_blueprint.route('/books/count', methods=['GET'])
def count_books():
    count = dao.count_books()
    return jsonify({'book_count': count}), 200


# pfad z.B /books/count_by_author?author=asdfasdf
@book_blueprint.route('/books/count_by_author', methods=['GET'])
def count_books_by_author():
    author = request.args.get('author')

    if author:
        # Die Closure aufrufen, um die Anzahl der Bücher des Autors zu zählen
        count_books_for_author = dao.count_books_by_author(author)
        count = count_books_for_author()
        return jsonify({'book_count': count, 'author': author}), 200
    else:
        return jsonify({'message': 'Author parameter is missing'}), 400


@book_blueprint.route('/books/filter', methods=['GET'])
def filter_books():
    is_read = request.args.get('is_read', type=bool)
    author = request.args.get('author', type=str)

    if is_read is not None and author:
        filtered_books = dao.get_books_by_status_and_author(is_read, author)
        return jsonify([book.__dict__ for book in filtered_books]), 200
    else:
        return jsonify({'message': 'Please provide both is_read and author parameters'}), 400
@book_blueprint.route('/books/uppercase_titles', methods=['GET'])
def get_uppercase_titles():
    titles = dao.get_uppercase_titles()
    return jsonify(titles), 200

@book_blueprint.route('/books/read_books_count', methods=['GET'])
def count_read_books():
    count = dao.count_read_books()
    return jsonify({'read_books_count': count}), 200

@book_blueprint.route('/books/uppercase_read_titles_count', methods=['GET'])
def get_uppercase_read_titles_count():
    count = dao.get_uppercase_read_titles_count()
    return jsonify({'uppercase_read_titles_count': count}), 200

@book_blueprint.route('/books/read_books_count_by_genre', methods=['GET'])
def get_read_books_count_by_genre():
    genre = request.args.get('genre')
    if genre:
        count = dao.get_read_books_count_by_genre(genre)
        return jsonify({'read_books_count_by_genre': count, 'genre': genre}), 200
    else:
        return jsonify({'message': 'Genre parameter is missing'}), 400