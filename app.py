from flask import Flask, jsonify, make_response, request
from flask_mongoengine import MongoEngine
from api_constants import mongodb_password

app = Flask(__name__)

database_name = "API"

DB_URL = "mongodb+srv://user:{}@socialmediacluster.elxk9mp.mongodb.net/{}?retryWrites=true&w=majority".format(
    mongodb_password, database_name)
app.config['MONGODB_HOST'] = DB_URL

db = MongoEngine()
db.init_app(app)


class Book(db.Document):
    book_id = db.IntField()
    name = db.StringField()
    author = db.StringField()

    def to_json(self):
        return {
            "book_id": self.book_id,
            "name": self.name,
            "author": self.author
        }


@app.route('/')
def index():

    return "Hello World"


@app.route('/api/db_populate/', methods=['POST'])
def db_populate():
    book1 = Book(book_id=1, name="Game of Thrones", author="Geargo RR Martin")
    book2 = Book(book_id=2, name="Lord of the Rings", author="JRR Tolkien")
    book1.save()
    book2.save()
    return make_response("", 201)


@app.route('/api/books/', methods=['POST', 'GET'])
def db_books():
    if request.method == "GET":
        books = []
        for book in Book.objects:
            books.append(book)
        return make_response(jsonify(books), 200)
    elif request.method == "POST":
        content = request.json
        book = Book(book_id=content['book_id'], name=content['name'],
                    author=content['author'])
        book.save()
        return make_response("", 201)


@app.route('/api/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def db_each_book(book_id):
    if request.method == "GET":
        book_obj = Book.objects(book_id=book_id).first()
        if book_obj:
            return make_response(jsonify(book_obj.to_json()), 200)
        else:
            return make_response("", 404)
    elif request.method == "PUT":
        content = request.json
        book_obj = Book(book_id=book_id).first()
        book_obj.update(author=content['author'], name=content['name'])
        return make_response("", 204)
    elif request.method == "DELETE":
        book_obj = Book(book_id=book_id).first()
        book_obj.delete()
        return make_response("")


if __name__ == '__main__':
    app.run(debug=True)
