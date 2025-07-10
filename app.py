from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view')
def view():
    with open("books.txt", "r") as f:
        books = [line.strip().split("|") for line in f.readlines()]
    return render_template("view.html", books=books)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        book_id = request.form['id']
        title = request.form['title']
        author = request.form['author']
        quantity = request.form['quantity']
        status = request.form['status']
        with open("books.txt", "a") as f:
            f.write(f"{book_id}|{title}|{author}|{quantity}|{status}\n")
        return redirect('/view')
    return render_template("add.html")

@app.route('/delete/<book_id>')
def delete_book(book_id):
    with open("books.txt", "r") as f:
        books = f.readlines()
    with open("books.txt", "w") as f:
        for book in books:
            if not book.startswith(book_id + "|"):
                f.write(book)
    return redirect('/view')

@app.route('/edit/<book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    with open("books.txt", "r") as f:
        books = f.readlines()

    selected_book = None
    updated_books = []

    for line in books:
        if line.startswith(book_id + "|"):
            selected_book = line.strip().split("|")
        else:
            updated_books.append(line)

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        quantity = request.form["quantity"]
        status = request.form["status"]
        new_line = f"{book_id}|{title}|{author}|{quantity}|{status}\n"
        updated_books.append(new_line)
        with open("books.txt", "w") as f:
            f.writelines(updated_books)
        return redirect("/view")

    return render_template("edit.html", book=selected_book)

@app.route('/search', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        query = request.form['query'].lower()
        with open("books.txt", "r") as f:
            for line in f:
                if query in line.lower():
                    results.append(line.strip().split("|"))
        return render_template("view.html", books=results)
    return render_template("search.html")

@app.route('/issue', methods=['GET', 'POST'])
def issue():
    if request.method == 'POST':
        book_id = request.form['book_id']
        with open("books.txt", "r") as f:
            books = f.readlines()
        updated_books = []
        for book in books:
            fields = book.strip().split('|')
            if fields[0] == book_id and int(fields[3]) > 0:
                fields[3] = str(int(fields[3]) - 1)
            updated_books.append("|".join(fields) + "\n")
        with open("books.txt", "w") as f:
            f.writelines(updated_books)
        return redirect('/view')
    return render_template("issue.html")

@app.route('/return', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        book_id = request.form['book_id']
        with open("books.txt", "r") as f:
            books = f.readlines()
        updated_books = []
        for book in books:
            fields = book.strip().split('|')
            if fields[0] == book_id:
                fields[3] = str(int(fields[3]) + 1)
            updated_books.append("|".join(fields) + "\n")
        with open("books.txt", "w") as f:
            f.writelines(updated_books)
        return redirect('/view')
    return render_template("Return.html")

if __name__ == '__main__':
    app.run(debug=True)
