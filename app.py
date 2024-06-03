from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    
    conn.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT, 
        author TEXT, 
        genre TEXT, 
        year INTEGER,
        status TEXT
    )
    ''')
    print("Table created successfully or already exists")
    
    # Check if the status column exists
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(books)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'status' not in columns:
        conn.execute("ALTER TABLE books ADD COLUMN status TEXT")
        print("Column 'status' added to the table")
    
    conn.close()

init_sqlite_db()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    conn.close()
    return render_template('index.html', books=books)

@app.route('/add/', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        status = request.form['status']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO books (title, author, genre, year, status) VALUES (?, ?, ?, ?, ?)", (title, author, genre, year, status))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/clear/', methods=['POST'])
def clear_data():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books")
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/update/<int:book_id>/', methods=['GET', 'POST'])
def update_book(book_id):
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        year = request.form['year']
        status = request.form['status']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE books SET title=?, author=?, genre=?, year=?, status=? WHERE id=?", (title, author, genre, year, status, book_id))
        conn.commit()
        conn.close()
        
        return redirect(url_for('index'))
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()
    conn.close()
    
    return render_template('update.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)
