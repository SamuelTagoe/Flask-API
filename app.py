import sqlite3

from flask import Flask, jsonify, request

app = Flask(__name__)


def db_connection():
    try:
        conn = sqlite3.connect("books.sqlite3")
        conn.row_factory = sqlite3.Row  # Allows fetching rows as dictionaries
        return conn
    except sqlite3.Error as error:
        print(error)
        return None


@app.route("/books", methods=["GET", "POST"])
def books():
    conn = db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()

    if request.method == "GET":
        cursor.execute("SELECT * FROM book")
        books = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(books), 200

    if request.method == "POST":
        data = request.json
        if (
            not data
            or "author" not in data
            or "language" not in data
            or "title" not in data
        ):
            return jsonify({"error": "Missing required fields"}), 400

        sql = "INSERT INTO book (author, language, title) VALUES (?, ?, ?)"
        cursor.execute(sql, (data["author"], data["language"], data["title"]))
        conn.commit()
        book_id = cursor.lastrowid
        conn.close()
        return jsonify({"message": f"Book with id {book_id} created successfully"}), 201


@app.route("/book/<int:id>", methods=["GET", "PUT", "DELETE"])
def single_book(id):
    conn = db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM book WHERE id=?", (id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return jsonify({"error": "Book not found"}), 404

    book = dict(row)

    if request.method == "GET":
        conn.close()
        return jsonify(book), 200

    if request.method == "PUT":
        data = request.json
        if (
            not data
            or "author" not in data
            or "language" not in data
            or "title" not in data
        ):
            return jsonify({"error": "Missing required fields"}), 400

        sql = "UPDATE book SET title=?, author=?, language=? WHERE id=?"
        cursor.execute(sql, (data["title"], data["author"], data["language"], id))
        conn.commit()
        conn.close()

        return jsonify({"message": f"Book with id {id} updated successfully"}), 200

    if request.method == "DELETE":
        cursor.execute("DELETE FROM book WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Book with id {id} deleted successfully"}), 200


if __name__ == "__main__":
    app.run(debug=True)
