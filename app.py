from flask import Flask, redirect, render_template, request

app = Flask(__name__)


def load_books():
    with open("books.txt", "r") as file:
        return [line.strip().split("|") for line in file if line.strip()]


def save_books(books):
    with open("books.txt", "w") as file:
        for book in books:
            file.write("|".join(book) + "\n")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/view")
def view():
    return render_template("view.html", books=load_books())


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        book_id = request.form["id"].strip()
        title = request.form["title"].strip()
        author = request.form["author"].strip()
        quantity = request.form["quantity"].strip()
        status = request.form["status"].strip()

        with open("books.txt", "a") as file:
            file.write(f"{book_id}|{title}|{author}|{quantity}|{status}\n")

        return redirect("/view")

    return render_template("add.html")


@app.route("/delete/<book_id>")
def delete_book(book_id):
    books = [book for book in load_books() if book[0] != book_id]
    save_books(books)
    return redirect("/view")


@app.route("/edit/<book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    books = load_books()
    selected_book = None
    updated_books = []

    for book in books:
        if book[0] == book_id:
            selected_book = book
        else:
            updated_books.append(book)

    if request.method == "POST":
        title = request.form["title"].strip()
        author = request.form["author"].strip()
        quantity = request.form["quantity"].strip()
        status = request.form["status"].strip()
        updated_books.append([book_id, title, author, quantity, status])
        save_books(updated_books)
        return redirect("/view")

    return render_template("edit.html", book=selected_book)


@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    if request.method == "POST":
        query = request.form["query"].strip().lower()
        for book in load_books():
            if query in "|".join(book).lower():
                results.append(book)
        return render_template("view.html", books=results)

    return render_template("search.html")


@app.route("/issue", methods=["GET", "POST"])
def issue():
    if request.method == "POST":
        book_id = request.form["book_id"].strip()
        updated_books = []

        for book in load_books():
            if book[0] == book_id and int(book[3]) > 0:
                book[3] = str(int(book[3]) - 1)
                if int(book[3]) == 0:
                    book[4] = "Issued"
            updated_books.append(book)

        save_books(updated_books)
        return redirect("/view")

    return render_template("issue.html")


@app.route("/return", methods=["GET", "POST"])
def return_book():
    if request.method == "POST":
        book_id = request.form["book_id"].strip()
        updated_books = []

        for book in load_books():
            if book[0] == book_id:
                book[3] = str(int(book[3]) + 1)
                book[4] = "Available"
            updated_books.append(book)

        save_books(updated_books)
        return redirect("/view")

    return render_template("return.html")


if __name__ == "__main__":
    app.run(debug=True)
