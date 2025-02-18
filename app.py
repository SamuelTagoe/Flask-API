from flask import Flask, jsonify, request

app = Flask(__name__)

books_list = [
    {
        "id": 1,
        "author": "John Smith",
        "language": "English",
        "title": "The Lost Horizon",
    },
    {
        "id": 2,
        "author": "Isabelle Dupont",
        "language": "French",
        "title": "L'Ombre du Temps",
    },
    {
        "id": 3,
        "author": "Carlos Mendoza",
        "language": "Spanish",
        "title": "El Secreto del Viento",
    },
    {
        "id": 4,
        "author": "Hans Gruber",
        "language": "German",
        "title": "Die Verborgene Wahrheit",
    },
    {
        "id": 5,
        "author": "Giovanni Ricci",
        "language": "Italian",
        "title": "Ombre e Luci",
    },
    {
        "id": 6,
        "author": "Li Wei",
        "language": "Chinese",
        "title": "风中的回忆",  # (Memories in the Wind)
    },
]


@app.route("/books", methods=["GET", "POST"])
def books():
    if request.method == "GET":
        if len(books_list) > 0:
            return jsonify({books_list})
        else:
            "Nothing found", 404

    if request.method == "POST":
        new_author = request.form["author"]
        new_lang = request.form["lang"]
        new_title = request.form["title"]
        iD = books_list[-1]["id"] + 1

        new_book = {
            "id": iD,
            "author": new_author,
            "language": new_lang,
            "title": new_title,
        }

        books_list.append(new_book)  # add new book encoding it into json
        return jsonify(new_book), 201


@app.route("/book/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_book(id):
    if request.method == "GET":
        for book in books_list:
            if book["id"] == id:
                return jsonify(book)
            pass
        return "Book not found", 404

    if request.method == "PUT":
        for book in books_list:
            if book["id"] == id:
                book["author"] = request.form["author"]
                book["language"] = request.form["lang"]
                book["title"] = request.form["title"]
                updated_book = {
                    "id": id,
                    "author": book["author"],
                    "language": book["language"],
                    "title": book["title"],
                }
                return jsonify(updated_book)
        return "Book not found", 404

    if request.method == "DELETE":
        for index, book in enumerate(books_list):
            if book["id"] == id:
                books_list.pop(index)
                return jsonify(books_list)
        return "Book not found", 404


if __name__ == "__main__":
    app.run(debug=True)
