import pytest
from parameterized import parameterized
from books_collector import BooksCollector

@pytest.fixture
def collector():
    """Создает новый экземпляр BooksCollector для каждого теста"""
    return BooksCollector()

# Тесты для добавления книг
def test_add_new_book_valid(collector):
    collector.add_new_book("Война и мир")
    assert "Война и мир" in collector.get_books_genre()
    assert collector.get_book_genre("Война и мир") == ''

@pytest.mark.parametrize("book_name, expected", [
    ("", False),
    ("a" * 41, False),
    (" ", False),
    ("Преступление и наказание", True),
])
def test_add_new_book_invalid(collector, book_name, expected):
    initial_count = len(collector.get_books_genre())
    collector.add_new_book(book_name)
    final_count = len(collector.get_books_genre())
    
    if expected:
        assert book_name in collector.get_books_genre()
        assert collector.get_book_genre(book_name) == ''
        assert final_count == initial_count + 1
    else:
        assert book_name not in collector.get_books_genre()
        assert final_count == initial_count

# Тесты для установки жанра
@pytest.mark.parametrize("book_name, genre, expected", [
    ("1984", "Фантастика", True),
    ("Мастер и Маргарита", "Ужасы", True),
    ("Неизвестная книга", "Фантастика", False),
    ("Война и мир", "Неизвестный жанр", False)
])
def test_set_book_genre(collector, book_name, genre, expected):
    if book_name != "Неизвестная книга":
        collector.add_new_book(book_name)
    collector.set_book_genre(book_name, genre)
    
    if expected:
        assert collector.get_book_genre(book_name) == genre
    else:
        assert collector.get_book_genre(book_name) == ''

# Тесты для получения жанра
def test_get_book_genre_existing(collector):
    collector.add_new_book("Дюна")
    collector.set_book_genre("Дюна", "Фантастика")
    assert collector.get_book_genre("Дюна") == "Фантастика"

def test_get_book_genre_nonexistent(collector):
    assert collector.get_book_genre("Неизвестная книга") is None

# Тесты для избранного
def test_add_nonexistent_to_favorites(collector):
    collector.add_book_in_favorites("Неизвестная книга")
    assert "Неизвестная книга" not in collector.get_list_of_favorites_books()

def test_delete_book_from_favorites(collector):
    collector.add_new_book("Гарри Поттер")
    collector.add_book_in_favorites("Гарри Поттер")
    collector.delete_book_from_favorites("Гарри Поттер")
    assert "Гарри Поттер" not in collector.get_list_of_favorites_books()

# Тесты для получения книг по жанру
def test_get_books_with_specific_genre(collector):
    collector.add_new_book("Дюна")
    collector.add_new_book("451 градус")
    collector.set_book_genre("Дюна", "Фантастика")
    collector.set_book_genre("451 градус", "Фантастика")
    result = collector.get_books_with_specific_genre("Фантастика")
    assert set(result) == {"Дюна", "451 градус"}

# Тесты для получения всех книг
def test_get_books_genre(collector):
    collector.add_new_book("Война и мир")
    collector.set_book_genre("Война и мир", "Классика")
    expected = {"Война и мир": "Классика"}
    assert collector.get_books_genre() == expected

# Тесты для детских книг
def test_get_books_for_children(collector):
    collector.add_new_book("Оно")
