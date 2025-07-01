from typing import List

from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str

class Book(BaseModel):
    id: int
    title: str
    author: str

class BorrowRequest(BaseModel):
    borrower: str
    title: str

class ReturnRequest(BaseModel):
    borrower: str
    title: str

class BorrowRecord(BaseModel):
    borrower: str
    title: str
    author: str

class BorrowerBooks(BaseModel):
    borrower: str
    books: List[str]
