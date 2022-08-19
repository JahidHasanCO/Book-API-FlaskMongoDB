from flask import Flask, jsonify, make_response, request, render_template
from flask_mongoengine import MongoEngine
from api_constants import mongodb_password


app = Flask(__name__, template_folder='templates')

database_name = "API"

DB_URL = "mongodb+srv://user:{}@socialmediacluster.elxk9mp.mongodb.net/{}?retryWrites=true&w=majority".format(
    mongodb_password, database_name)
app.config['MONGODB_HOST'] = DB_URL

db = MongoEngine()
db.init_app(app)


class Book(db.Document):
    book_id = db.IntField()
    title = db.StringField()
    author = db.StringField()
    publisher = db.StringField()
    publishedDate = db.StringField()
    description = db.StringField()
    pageCount = db.StringField()
    printedPageCount = db.StringField()
    language = db.StringField()
    printType = db.StringField()
    averageRating = db.DoubleField()
    maturityRating = db.StringField()
    ratingsCount = db.IntField()
    imageLinks = []

    def to_json(self):

        VolumnInfo = {
            "title": self.title,
            "author": self.author,
            "publisher": self.publisher,
            "publishedDate": self.publishedDate,
            "description": self.description,
            "pageCount": self.pageCount,
            "printedPageCount": self.printedPageCount,
        }
        return {
            "book_id": self.book_id,
            "VolumnInfo": VolumnInfo,
            "imageLinks": self.imageLinks,
            "language": self.language,
            "printType": self.printType,
            "averageRating": self.averageRating,
            "ratingsCount": self.ratingsCount,
            "maturityRating": self.maturityRating
        }


@app.route('/')
def index():

    return render_template("index.html")


# Book(book_id =1,
#     title = "",
#     author =,
#      publisher=,
#      publishedDate=,
#      description=,
#      pageCount=,
#      printedPageCount=,
#      language=,
#      printType=,
#      averageRating=,
#      maturityRating=,
#      ratingsCount=,
#      imageLinks=)

@app.route('/api/db_populate/', methods=['POST'])
def db_populate():
    images = []
    book1 = Book(book_id=1,
                 title="Pride and Prejudice",
                 author="Jane Austen",
                 publisher="C. Scribner's sons",
                 publishedDate="1918",
                 description="Austen’s most celebrated novel tells the story of Elizabeth Bennet, a bright, lively young woman with four sisters, and a mother determined to marry them to wealthy men. At a party near the Bennets’ home in the English countryside, Elizabeth meets the wealthy, proud Fitzwilliam Darcy. Elizabeth initially finds Darcy haughty and intolerable, but circumstances continue to unite the pair. Mr. Darcy finds himself captivated by Elizabeth’s wit and candor, while her reservations about his character slowly vanish. The story is as much a social critique as it is a love story, and the prose crackles with Austen’s wry wit.",
                 pageCount=401,
                 printedPageCount=448,
                 language="en",
                 printType="BOOK",
                 averageRating=4,
                 maturityRating="NOT_MATURE",
                 ratingsCount=400,
                 imageLinks=images)
    book1.save()
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
        book = Book(book_id=content['book_id'],
                    title=content['title'],
                    author=content['author'],
                    publisher=content['publisher'],
                    publishedDate=content['publishedDate'],
                    description=content['description'],
                    pageCount=content['pageCount'],
                    printedPageCount=content['printedPageCount'],
                    language=content['language'],
                    printType=content['printType'],
                    averageRating=content['averageRating'],
                    maturityRating=content['maturityRating'],
                    ratingsCount=content['ratingsCount'],
                    imageLinks=content['imageLinks'])
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
        book_obj.update(book_id=content['book_id'],
                        title=content['title'],
                        author=content['author'],
                        publisher=content['publisher'],
                        publishedDate=content['publishedDate'],
                        description=content['description'],
                        pageCount=content['pageCount'],
                        printedPageCount=content['printedPageCount'],
                        language=content['language'],
                        printType=content['printType'],
                        averageRating=content['averageRating'],
                        maturityRating=content['maturityRating'],
                        ratingsCount=content['ratingsCount'],
                        imageLinks=content['imageLinks'])
        return make_response("", 204)
    elif request.method == "DELETE":
        book_obj = Book(book_id=book_id).first()
        book_obj.delete()
        return make_response("")


if __name__ == '__main__':
    app.run(debug=True)
