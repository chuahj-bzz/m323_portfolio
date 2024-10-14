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
