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
def test_add_nonexistent_to_favorites():
    collector = BooksCollector()
    collector.add_book_in_favorites("Неизвестная книга")
    assert "Неизвестная книга" not in collector.get_list_of_favorites_books()

def test_delete_book_from_favorites():
    collector = BooksCollector()
    collector.add_new_book("Гарри Поттер")
    collector.add_book_in_favorites("Гарри Поттер")
    collector.delete_book_from_favorites("Гарри Поттер")
    assert "Гарри Поттер" not in collector.get_list_of_favorites_books()
    # Тесты для получения книг по жанру
def test_get_books_with_specific_genre():
    collector = BooksCollector()
    collector.add_new_book("Дюна")
    collector.add_new_book("451 градус")
    collector.set_book_genre("Дюна", "Фантастика")
    collector.set_book_genre("451 градус", "Фантастика")
    
    result = collector.get_books_with_specific_genre("Фантастика")
    assert set(result) == {"Дюна", "451 градус"}

# Тесты для получения всех книг
def test_get_books_genre():
    collector = BooksCollector()
    collector.add_new_book("Война и мир")
    collector.set_book_genre("Война и мир", "Классика")
    expected = {"Война и мир": "Классика"}
    assert collector.get_books_genre() == expected

# Тесты для детских книг
def test_get_books_for_children():
    collector = BooksCollector()
    collector.add_new_book("Оно")
    collector.add_new_book("Король Лев")
    collector.add_new_book("Смешарики")
    collector.set_book_genre("Оно", "Ужасы")
    collector.set_book_genre("Король Лев", "Мультфильмы")
    collector.set_book_genre("Смешарики", "Комедии")
    
    result = collector.get_books_for_children()
    assert set(result) == {"Король Лев", "Смешарики"}

# Дополнительные тесты для избранного
def test_add_duplicate_to_favorites():
    collector = BooksCollector()
    collector.add_new_book("Гарри Поттер")
    collector.add_book_in_favorites("Гарри Поттер")
    collector.add_book_in_favorites("Гарри Поттер")
    assert collector.get_list_of_favorites_books() == ["Гарри Поттер"]
   
def test_empty_state_on_init():
    collector = BooksCollector()
    assert collector.get_books_genre() == {}
    assert collector.get_list_of_favorites_books() == []

def test_empty_favorites_list():
    collector = BooksCollector()
    assert collector.get_list_of_favorites_books() == []
    

