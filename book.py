from dataclasses import dataclass

@dataclass(frozen=True)
class Book:
    book_id: int
    title: str
    author: str
    genre: str
    is_read: bool

    def __str__(self):
        return f"{self.title} by {self.author}, Genre: {self.genre}, Read: {self.is_read}"

# Pure Function: Überprüft, ob ein Buch als gelesen markiert wurde
def is_read_status(book: Book) -> bool:
    return book.is_read
