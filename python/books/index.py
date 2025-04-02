from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({"books": ["Book 1", "Book 2", "Book 3"]})