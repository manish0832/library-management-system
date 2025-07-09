from flask import Flask, render_template, request, redirect, jsonify

app = Flask(__name__)
BOOKS_FILE = "books.txt"

def read_books():
    try:
        with open(BOOKS_FILE, "r") as f:
            return [line.strip().split(",") for line in f]
    except FileNotFoundError:
        return []

def write_books(books):
    with open(BOOKS_FILE, "w") as f:
        for book in books:
            f.write(",".join(book) + "\n")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        book = [
            request.form['id'],
            request.form['title'],
            request.form['author'],
            request.form['quantity'],
            "Available"
        ]
        with open(BOOKS_FILE, "a") as f:
            f.write(",".join(book) + "\n")
        return redirect("/view")
    return render_template("add.html")

@app.route("/view")
def view_books():
    books = read_books()
    return render_template("view.html", books=books)

@app.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").lower()
    results = [book for book in read_books() if query in book[1].lower() or query in book[2].lower()]
    return render_template("search.html", books=results, query=query)

@app.route("/issue", methods=["GET", "POST"])
def issue_book():
    if request.method == "POST":
        book_id = request.form['id']
        books = read_books()
        for book in books:
            if book[0] == book_id and book[4] == "Available" and int(book[3]) > 0:
                book[3] = str(int(book[3]) - 1)
                if int(book[3]) == 0:
                    book[4] = "Issued"
                write_books(books)
                return redirect("/view")
        return "Cannot issue book"
    return render_template("issue.html")

@app.route("/return", methods=["GET", "POST"])
def return_book():
    if request.method == "POST":
        book_id = request.form['id']
        books = read_books()
        for book in books:
            if book[0] == book_id:
                book[3] = str(int(book[3]) + 1)
                book[4] = "Available"
                write_books(books)
                return redirect("/view")
        return "Book not found"
    return render_template("return.html")

if __name__ == "__main__":
    app.run(debug=True)
