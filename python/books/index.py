from flask import Flask, jsonify, request

from books.model.book import Book, BookSchema

app = Flask(__name__)

books = [
    Book(1, "Book 1", "Author 1"),
    Book(2, "Book 2", "Author 2"),
    Book(3, "Book 3", "Author 3"),
]

@app.route('/books', methods=['GET'])
def get_books():
    schema = BookSchema(many=True)
    return jsonify(schema.dump(books))

@app.route('/books', methods=['POST'])
def add_income():
    books.append(request.get_json())
    return books, 201