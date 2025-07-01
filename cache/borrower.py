from typing import List

from . import redis_client

def test():
    return "redis connect ok"

def _borrower_key(borrower: str) -> str:
    """대출자별 키 문자열 생성"""
    return f"borrower:{borrower}:books"
class Borrower:
    @classmethod
    def add_book_for_borrower(cls, borrower: str, title: str) -> None:
        """
        대출자 키에 도서 제목을 추가합니다.
        중복을 방지하려면 필요한 경우 set 자료구조로 변경할 수 있습니다.
        """
        key = _borrower_key(borrower)
        redis_client.rpush(key, title)

    @classmethod
    def remove_book_for_borrower(cls, borrower: str, title: str) -> None:
        """
        대출자 키에서 도서 제목을 제거합니다.
        list의 모든 동일 항목을 제거합니다.
        """
        key = _borrower_key(borrower)
        redis_client.lrem(key, 0, title)

    @classmethod
    def get_books_for_borrower(cls, borrower: str) -> List[str]:
        """
        대출자 키에 저장된 모든 도서 제목 목록을 반환합니다.
        """
        key = _borrower_key(borrower)
        return redis_client.lrange(key, 0, -1)



