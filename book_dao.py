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

    # closure
    def count_books_by_author(self, author: str):
        def is_author(book: Book) -> bool:
            return book.author == author

        def count_books() -> int:
            books = self.get_all_books()
            return len(list(filter(is_author, books)))

        return count_books

    def get_books_by_status_and_author(self, is_read: bool, author: str):
        books = self.get_all_books()
        return list(filter(lambda book: book.is_read == is_read and book.author == author, books))

    # sorted
    def sort_books_by(self, criteria: str, descending: bool = False):
        books = self.get_all_books()
        if criteria == 'title':
            return sorted(books, key=lambda book: book.title, reverse=descending)
        elif criteria == 'author':
            return sorted(books, key=lambda book: book.author, reverse=descending)
        elif criteria == 'genre':
            return sorted(books, key=lambda book: book.genre, reverse=descending)
        else:
            raise ValueError(f"Sorting by {criteria} is not supported.")

    # b4 kompetenze
    def get_read_books(self):
        books = self.get_all_books()
        return list(filter(lambda book: book.is_read, books))

    # Map: Alle Buchtitel in Großbuchstaben umwandeln
    def get_uppercase_titles(self):
        books = self.get_all_books()
        return list(map(lambda book: book.title.upper(), books))

    # Reduce: Gesamtanzahl der gelesenen Bücher zählen
    def count_read_books(self):
        books = self.get_all_books()
        return reduce(lambda count, book: count + (1 if book.is_read else 0), books, 0)

    def get_uppercase_read_titles_count(self):
        books = self.get_all_books()
        read_books = filter(lambda book: book.is_read, books)
        uppercase_titles = map(lambda book: book.title.upper(), read_books)
        return reduce(lambda count, _: count + 1, uppercase_titles, 0)

    def get_read_books_count_by_genre(self, genre):
        books = self.get_all_books()
        read_books_in_genre = filter(lambda book: book.is_read and book.genre == genre, books)
        return reduce(lambda count, _: count + 1, read_books_in_genre, 0)
