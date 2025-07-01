from typing import List, Any

from data import borrowings as data
from cache.borrower import Borrower as cache
from web.model.book import BookCreate, BorrowRecord, BorrowerBooks


def row_to_BookCreate(row):
    return BookCreate(
        title=row[0],
        author=row[1],
    )
def row_to_BorrowRecord(row):
    return BorrowRecord(
        borrower=row[0],
        title=row[1],
        author=row[2],
    )
class BorrowingService:

    @classmethod
    def add_book(cls, title, author):
        return data.add_book(title, author)


    @classmethod
    def list_available_books(cls) -> List[BookCreate]:
        return [row_to_BookCreate(d) for d in data.get_available_books()]

    @classmethod
    def delete_book(cls, book_id):
        if data.available_book(book_id):
            data.delete_book(book_id)
            return True
        return False


    @classmethod
    def borrow_book(cls, borrower, title):
        try:
            book_id = data.get_bookid_by_title(title)[0]
            if data.available_book(book_id):
                data.borrow_book(book_id)
                data.borrow(book_id, borrower)
                cache.add_book_for_borrower(borrower, title)
                return True
            return None
        except Exception as e:
            print(e)
            return False

    @classmethod
    def get_borrows_by_month(cls, borrow_month) -> List[BorrowRecord]:
        return [row_to_BorrowRecord(r) for r in data.get_borrows_by_month(borrow_month)]

    @classmethod
    def get_borrowed_books(cls, borrower) -> list[Any] | BorrowerBooks:
        try:
            return BorrowerBooks(
                borrower=borrower,
                books=cache.get_books_for_borrower(borrower)
            )
        except Exception as e:
            print(e)
            return []

    @classmethod
    def return_book(cls, borrower, title):
        try:
            print("hi")
            book_id = data.get_bookid_by_title(title)[0]
            print("hi")
            print(data.available_book(book_id))
            if data.available_book(book_id)[0] == 0:

                l = data.return_book(borrower, book_id)
                r = data.book_availe(book_id)
                print(l, r)
                cache.remove_book_for_borrower(borrower, title)
                return True
            return None
        except Exception as e:
            print(e)
            return False