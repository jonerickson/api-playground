import datetime as dt
import database.sqlite as db

from marshmallow import Schema, fields, validate 

class Book(object):
    def __init__(self, title=None, author=None, id=None):
        self.id = id
        self.title = title
        self.author = author

    def __repr__(self):
        return f'<Book(id={self.id}, title={self.title!r}, author={self.author!r})>'
    
    @classmethod
    def get_all(cls):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author FROM books")
        books = [cls(id=row[0], title=row[1], author=row[2]) for row in cursor.fetchall()]
        conn.close()

        if books:
            return books
        return None
    
    @classmethod
    def get_by_id(cls, id):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, author FROM books WHERE id = ?", (str(id)))
        row = cursor.fetchone()
        conn.close()

        if row:
            return cls(id=row[0], title=row[1], author=row[2])
        return None
    
    @classmethod
    def create(cls, title, author):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
        conn.commit()
        id = cursor.lastrowid
        conn.close()
        return Book(id=id, title=title, author=author)

    def update(self, title=None, author=None):
        if not self.id:
            raise ValueError("Cannot update a book without an ID.")
        
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET title = ?, author = ? WHERE id = ?", (title, author, str(self.id)))
        conn.commit()
        if title: self.title = title
        if author: self.author = author
        conn.close()
        return self

    def delete(self):
        if not self.id:
            raise ValueError("Cannot update a book without an ID.")
        
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books WHERE id = ?", (str(self.id)))
        conn.commit()
        conn.close()
        return True
    
class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1))
    author = fields.Str(required=True, validate=validate.Length(min=1))
