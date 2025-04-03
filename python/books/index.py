import database.sqlite as db
import os

from flask import Flask, jsonify, request
from marshmallow import ValidationError
from books.model.book import Book, BookSchema

app = Flask(__name__)

@app.route('/books', methods=['GET'])
def get_books():    
    return jsonify({"data": BookSchema(many=True).dump(Book.get_all())})

@app.route('/books/<int:id>', methods=['GET'])
def get_book_by_id(id):
    book = Book.get_by_id(id)

    if book is None:
        return jsonify({"error": "Book not found."}), 404
    
    return jsonify({"data": BookSchema().dump(book)})

@app.route('/books', methods=['POST'])
def create_book():
    try:
        data = BookSchema().load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422 
    
    book = Book().create(
        title=data["title"], 
        author=data["author"]
    )
    
    return jsonify({"data": BookSchema().dump(book)}), 201

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.get_by_id(id)

    if book is None:
        return jsonify({"error": "Book not found."}), 404
    
    try:
        data = BookSchema(partial=True).load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422
    
    book.update(
        title=data.get('title', book.title), 
        author=data.get('author', book.author)
    )
    
    return jsonify({"data": BookSchema().dump(book)})

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.get_by_id(id)

    if book is None:
        return jsonify({"error": "Book not found."}), 404
    
    book.delete()
    
    return '', 204

db.init_db()

print(f"""
Environment Variables:
      
DATABASE_PATH={os.getenv('DATABASE_PATH')}
""")