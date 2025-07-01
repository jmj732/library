from datetime import datetime

from . import con, cur

def test():
    return "sqlite connect ok"


def add_book(title, author):
    try:
        sql = "INSERT INTO books (title, author) VALUES (?, ?)"
        cur.execute(sql, (title, author))
        con.commit()
        return True
    except Exception as e:
        con.rollback()
        return False


def get_available_books():
    sql = "SELECT title,author FROM books where available=1"
    cur.execute(sql)
    return cur.fetchall()


def available_book(book_id):
    try:
        sql = "SELECT available FROM books where book_id=?"
        cur.execute(sql, (book_id,))
        return cur.fetchone()
    except Exception as e:
        con.rollback()
        return False

def delete_book(book_id):
    sql = "DELETE FROM books WHERE book_id=?"
    cur.execute(sql, (book_id,))
    con.commit()
    return True


def get_bookid_by_title(title):
    sql = "SELECT book_id FROM books WHERE title=?"
    cur.execute(sql, (title,))
    return cur.fetchone()


def borrow_book(book_id):
    sql = "UPDATE books SET available=0 WHERE book_id=?"
    cur.execute(sql, (book_id,))
    con.commit()
    return


def borrow(book_id, borrower):
    sql = "insert into borrowings (book_id, borrower) VALUES (?, ?)"
    cur.execute(sql, (book_id, borrower))
    con.commit()
    return None


def get_borrows_by_month(borrow_month):
    sql = "select b.borrower,bo.title,bo.author from borrowings b join books bo on b.book_id = bo.book_id where strftime('%m', b.borrowed_at) = printf('%02d', ?);"
    cur.execute(sql, (borrow_month,))
    return cur.fetchall()


def get_borrower_record(borrower):
    sql = "select book_id from borrowings where borrower=?"
    cur.execute(sql,(borrower,))
    return cur.fetchall()


def get_book_name(id):
    sql = "select title from books where id=?"
    cur.execute(sql,(id,))
    return cur.fetchone()


def return_book(borrower, book_id):
    sql = "update borrowings set returned_at = ? where book_id=? and borrower=?"
    cur.execute(sql,(datetime.now().isoformat(sep=' '), book_id, borrower))

    updated = cur.rowcount
    con.commit()
    return updated > 0


def book_availe(book_id):
    sql = "update books set available=1 where book_id=?"
    cur.execute(sql,(book_id,))
    con.commit()
    return True