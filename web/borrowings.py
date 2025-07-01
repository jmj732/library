from fastapi import APIRouter, HTTPException
from typing import List
from web.model.book import BookCreate, Book, BorrowRequest, BorrowRecord, BorrowerBooks, ReturnRequest
from service.borrowings import BorrowingService as service
router = APIRouter()

# --- Routes ---
@router.post("/books", response_model=bool)
def create_book(book: BookCreate):
    """도서 등록"""
    success = service.add_book(book.title, book.author)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to register book.")
    return True

@router.get("/books", response_model=List[BookCreate])
def list_books():
    """대출 가능한 도서 목록 조회"""
    return service.list_available_books()

@router.delete("/books/{book_id}", response_model=bool)
def delete_book(book_id: int):
    """도서 삭제"""
    success = service.delete_book(book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found or not available.")
    return True

@router.post("/borrows", response_model=bool)
def borrow_book(request: BorrowRequest):
    """도서 대출 처리"""
    success = service.borrow_book(request.borrower, request.title)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to borrow book.")
    return True

@router.get("/borrows/month/{borrow_month}", response_model=List[BorrowRecord])
def get_borrows_by_month(borrow_month: int):
    """월별 대출 기록 조회"""
    return service.get_borrows_by_month(borrow_month)

@router.get("/borrowers/{borrower}/books", response_model=BorrowerBooks)
def get_borrower_books(borrower: str) -> BorrowerBooks:
    """특정 대출자의 대출 기록 조회"""
    return service.get_borrowed_books(borrower)

@router.post("/return", response_model=bool)
def return_book(request: ReturnRequest):
    """도서 반납 처리"""
    success = service.return_book(request.borrower, request.title)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to return book.")
    return True
