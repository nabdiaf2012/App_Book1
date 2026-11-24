"""
Book CRUD API
Adapted from the "REST API Crash Course" (Drink API example)
Model Fields: id, book_name, author, publisher
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Initialize the Flask application
app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database object
db = SQLAlchemy(app)


# ----------------------------
# 1. Define the Book Model
# ----------------------------
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    publisher = db.Column(db.String(150), nullable=True)

    def to_dict(self):
        """Helper method to serialize the Book object to JSON."""
        return {
            'id': self.id,
            'book_name': self.book_name,
            'author': self.author,
            'publisher': self.publisher
        }


# Create the database tables within the application context
with app.app_context():
    db.create_all()


# ----------------------------
# 2. CRUD Endpoints
# ----------------------------

# GET /books -> Retrieve all books
@app.route('/books', methods=['GET'])
def get_all_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books]), 200


# GET /books/<id> -> Retrieve a single book by its ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404
    return jsonify(book.to_dict()), 200


# POST /books -> Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()

    # Validate required fields
    if not data or 'book_name' not in data or 'author' not in data:
        return jsonify({'error': 'book_name and author are required'}), 400

    new_book = Book(
        book_name=data['book_name'],
        author=data['author'],
        publisher=data.get('publisher')  # publisher is optional
    )

    db.session.add(new_book)
    db.session.commit()

    return jsonify(new_book.to_dict()), 201


# PUT /books/<id> -> Update an existing book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404

    data = request.get_json()

    # Update fields if they are provided
    if 'book_name' in data:
        book.book_name = data['book_name']
    if 'author' in data:
        book.author = data['author']
    if 'publisher' in data:
        book.publisher = data['publisher']

    db.session.commit()

    return jsonify(book.to_dict()), 200


# DELETE /books/<id> -> Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({'error': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book deleted successfully'}), 200


# ----------------------------
# 3. Run the Application
# ----------------------------
if __name__ == '__main__':
    app.run(debug=True)