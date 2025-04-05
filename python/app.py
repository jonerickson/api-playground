import os

from datetime import timedelta
from flask import Flask, jsonify, request, Response
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError

def print_env():
    print(" * Environment Variables:")
    print(" * - JWT_SECRET:", os.getenv('JWT_SECRET'))
    print(" * - DATABASE_URL:", os.getenv('DATABASE_URL'))

def create_app():
    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET')
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///../database.sqlite')
    print_env()
    return app

app = create_app()
jwt = JWTManager(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

class ApiException(Exception):
    def __init__(self, message, code):
        self.message = message
        self.code = code

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def __repr__(self):
        return f'<Book(id={self.id}, title={self.title!r}, author={self.author!r})>'
    
class BookSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Book
        
book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route('/', methods=['GET'])
def index():    
    return jsonify({"message": "Okay", "language": "Python", "framework": "Flask", "packages": ["Flask", "Flask-JWT-Extended", "Flask-SQLAlchemy", "Flask-Marshmallow"]})

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

# GET ALL
@app.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    books = Book.query.all() 
    
    return books_schema.jsonify(books)

# GET BY ID
@app.route('/books/<int:id>', methods=['GET'])
@jwt_required()
def get_book_by_id(id):
    book = Book.query.get(id)

    if book is None:
        raise ApiException("The book could not be found.", 404)
    
    return book_schema.jsonify(book)

# CREATE
@app.route('/books', methods=['POST'])
@jwt_required()
def create_book():
    try:
        data = book_schema.load(request.get_json())
    except ValidationError as err:
        raise ApiException(err.messages, 422)
    
    book = Book(title=data["title"], author=data["author"])

    db.session.add(book)
    db.session.commit()
    
    return book_schema.jsonify(book), 201

# UPDATE
@app.route('/books/<int:id>', methods=['PUT'])
@jwt_required()
def update_book(id):
    book = Book.query.get(id)

    if book is None:
        raise ApiException("The book could not be found.", 404)
    
    try:
        data = book_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        raise ApiException(err.messages, 422)

    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    
    db.session.add(book)
    db.session.commit()
    
    return book_schema.jsonify(book)

# DELETE
@app.route('/books/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    book = Book.query.get(id)

    if book is None:
        raise ApiException("The book could not be found.", 404)
    
    db.session.delete(book)
    db.session.commit()    

    return '', 204

@app.after_request
def wrap_response(response: Response) -> Response:
    if response.content_type != 'application/json' or not response.get_data():
        return response

    original_data = response.get_json()
    status_code = response.status_code

    status = "okay" if 200 <= status_code < 400 else "error"

    wrapped_data = {
        "status": status,
    }

    if status == "okay":
        wrapped_data["data"] = original_data

    if status == "error":
        wrapped_data["error"] = original_data["error"] if "error" in original_data else original_data

    new_response = jsonify(wrapped_data)
    new_response.status_code = status_code

    return new_response

@app.errorhandler(Exception)
def handle_exception(e):
    status_code = 500
    error_message = str(e)

    if isinstance(e, ApiException):
        status_code = str(e.code)
        error_message = str(e.message)
    else:
        app.logger.error(f"Unhandled exception: {str(e)}")

    return jsonify({"error": error_message}), status_code