import sqlite3
from functools import reduce
from book import Book, is_read_status

class BookDao:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_table(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS books (
                    book_id INTEGER PRIMARY KEY,
                    title TEXT,
                    author TEXT,
                    genre TEXT,
                    is_read BOOLEAN
                )
            """)
            conn.commit()

    def add_book(self, book: Book):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO books (title, author, genre, is_read) VALUES (?, ?, ?, ?)",
                (book.title, book.author, book.genre, book.is_read)
            )
            conn.commit()

    def get_all_books(self) -> list:
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            rows = cursor.fetchall()
            return [Book(row[0], row[1], row[2], row[3], row[4]) for row in rows]

    def count_books(self) -> int:
        books = self.get_all_books()
        return len(list(filter(lambda book: is_read_status(book), books)))

    def delete_book(self, book_id: int) -> bool:
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE book_id=?", (book_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_book_by_id(self, book_id: int) -> Book:
        # Optimized Refactored function to only query the database once
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books WHERE book_id=?", (book_id,))
            row = cursor.fetchone()
            return Book(*row) if row else None
