import pytest
from main import BooksCollector  # Только импорт, без класса

# Тесты должны быть разделены на отдельные методы
# Каждый тест - один сценарий

def test_add_new_book_valid():
    collector = BooksCollector()
    collector.add_new_book("Война и мир")
    assert "Война и мир" in collector.get_books_genre()
    assert collector.get_book_genre("Война и мир") == ''

def test_add_new_book_empty_name():
    collector = BooksCollector()
    collector.add_new_book("")
    assert "" not in collector.get_books_genre()

def test_add_new_book_too_long():
    collector = BooksCollector()
    collector.add_new_book("a" * 41)
    assert "a" * 41 not in collector.get_books_genre()

@pytest.mark.parametrize("book_name, genre, expected", [
    ("1984", "Фантастика", True),  # книга есть, жанр допустимый
    ("Мастер и Маргарита", "Ужасы", True),  # книга есть, жанр допустимый
    ("Неизвестная книга", "Фантастика", False),  # книги нет в словаре
    ("Война и мир", "Неизвестный жанр", False)  # недопустимый жанр
])
def test_set_book_genre(book_name, genre, expected):
    collector = BooksCollector()
    if book_name != "Неизвестная книга":
        collector.add_new_book(book_name)
    collector.set_book_genre(book_name, genre)
    
    if expected:
        assert collector.get_book_genre(book_name) == genre
    else:
        assert collector.get_book_genre(book_name) == ''

def test_get_book_genre_existing():
    collector = BooksCollector()
    collector.add_new_book("Дюна")
    collector.set_book_genre("Дюна", "Фантастика")
    assert collector.get_book_genre("Дюна") == "Фантастика"

def test_get_book_genre_nonexistent():
    collector = BooksCollector()
    assert collector.get_book_genre("Неизвестная книга") is None

# Аналогично переписать остальные тесты, следуя этим принципам:
# - создавать экземпляр класса внутри каждого теста
# - один сценарий на тест
# - использовать pytest.mark.parametrize вместо parameterized
# - убрать setUp
