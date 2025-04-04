import database.sqlite as db
from datetime import timedelta
import os

from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from marshmallow import ValidationError
from books.model.book import Book, BookSchema

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    return app

app = create_app()
jwt = JWTManager(app)

@app.route('/', methods=['GET'])
def index():    
    return jsonify({"message": "Okay", "language": "Python", "framework": "Flask"})

@app.route("/login", methods=["POST"])
def login():
    username = request.authorization.username
    password = request.authorization.password
    if username != "test" or password != "test":
        return jsonify({"error": "Bad username or password."}), 401

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token, "type": "bearer", "expires_in": 3600})

@app.route("/me", methods=["GET"])
@jwt_required()
def me():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

@jwt_required()
@app.route('/books', methods=['GET'])
def get_books():    
    return jsonify({"data": BookSchema(many=True).dump(Book.get_all())})

@jwt_required()
@app.route('/books/<int:id>', methods=['GET'])
def get_book_by_id(id):
    book = Book.get_by_id(id)

    if book is None:
        return jsonify({"error": "The book could not be found."}), 404
    
    return jsonify({"data": BookSchema().dump(book)})

@jwt_required()
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

@jwt_required()
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.get_by_id(id)

    if book is None:
        return jsonify({"error": "The book could not be found."}), 404
    
    try:
        data = BookSchema(partial=True).load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422
    
    book.update(
        title=data.get('title', book.title), 
        author=data.get('author', book.author)
    )
    
    return jsonify({"data": BookSchema().dump(book)})

@jwt_required()
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.get_by_id(id)

    if book is None:
        return jsonify({"error": "The book could not be found."}), 404
    
    book.delete()
    
    return '', 204

db.init_db()

print(f"""
Environment Variables:
      
DATABASE_PATH={os.getenv('DATABASE_PATH')}
JWT_SECRET={os.getenv('JWT_SECRET')}
""")