from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mmafya79@localhost:3306/book'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {"id": self.id, "author": self.author, "language": self.language, "title": self.title}

@app.route('/books', methods=['GET', 'POST'])
def books():
    if request.method == 'GET':
        books = Book.query.all()
        book_list = [book.to_dict() for book in books]
        return jsonify(book_list)

    if request.method == 'POST':
        try:
            new_author = request.json['author']
            new_lang = request.json['language']
            new_title = request.json['title']

            new_book = Book(author=new_author, language=new_lang, title=new_title)

            db.session.add(new_book)
            db.session.commit()

            return jsonify({"message": "Book added successfully"}), 201

        except Exception as e:
            print(e)
            return jsonify({"error": "Invalid data format"}), 400

@app.route('/books/<int:book_id>', methods=['PUT', 'DELETE'])
def book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    if request.method == 'PUT':
        try:
            data = request.json
            book.author = data.get('author', book.author)
            book.language = data.get('language', book.language)
            book.title = data.get('title', book.title)

            db.session.commit()

            return jsonify({"message": "Book updated successfully"}), 200

        except Exception as e:
            print(e)
            return jsonify({"error": "Invalid data format"}), 400

    if request.method == 'DELETE':
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
