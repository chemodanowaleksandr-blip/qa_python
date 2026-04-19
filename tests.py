from main import BooksCollector
import pytest

# обязательно указывать префикс Test
class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self):
        # создаем экземпляр (объект) класса BooksCollector
        collector = BooksCollector()
        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        assert len(collector.get_books_genre()) == 2

    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    @pytest.mark.parametrize("book_name, expected_result", [
        ("Короткий заголовок", True),
        ("", False),  # пустая строка
        ("a" * 41, False),  # длиннее 40 символов
    ])
    def test_add_new_book_valid_and_invalid_names(self, book_name, expected_result):
        collector = BooksCollector()
        initial_count = len(collector.get_books_genre())
        collector.add_new_book(book_name)
        final_count = len(collector.get_books_genre())

        if expected_result:
            assert final_count == initial_count + 1
            assert book_name in collector.get_books_genre()
        else:
            assert final_count == initial_count

    @pytest.mark.parametrize("genre, is_valid", [
        ("Фантастика", True),
        ("Ужасы", True),
        ("Романтика", False),  # не в списке доступных жанров
    ])
    def test_set_book_genre_valid_and_invalid_genres(self, genre, is_valid):
        collector = BooksCollector()
        book_name = "Новый роман"
        collector.add_new_book(book_name)

        collector.set_book_genre(book_name, genre)
        current_genre = collector.get_book_genre(book_name)

        if is_valid:
            assert current_genre == genre
        else:
            assert current_genre == ""  # жанр не изменился

    def test_get_books_with_specific_genre_returns_correct_list(self):
        collector = BooksCollector()
        books_data = [
            ("Гарри Поттер", "Фэнтези"),
            ("Шерлок Холмс", "Детективы"),
            ("Алиса в Стране чудес", "Фэнтези")
        ]

        for book, genre in books_data:
            collector.add_new_book(book)
            collector.set_book_genre(book, genre)

        fantasy_books = collector.get_books_with_specific_genre("Фэнтези")
        assert fantasy_books == ["Гарри Поттер", "Алиса в Стране чудес"]

    def test_get_books_for_children_excludes_age_rated_genres(self):
        collector = BooksCollector()
        # Книги с возрастным рейтингом (не должны попасть в список)
        collector.add_new_book("Оно")
        collector.set_book_genre("Оно", "Ужасы")  # 'Ужасы' в genre_age_rating

        # Книги без возрастного рейтинга (должны попасть в список)
        collector.add_new_book("Том и Джерри")
        collector.set_book_genre("Том и Джерри", "Мультфильмы")

        children_books = collector.get_books_for_children()
        assert "Том и Джерри" in children_books
        assert "Оно" not in children_books

    @pytest.mark.parametrize("book_name, should_be_added", [
        ("Существующая книга", True),  # книга есть в словаре
        ("Несуществующая книга", False),  # книги нет в словаре
    ])
    def test_add_book_in_favorites_valid_and_invalid_books(self, book_name, should_be_added):
        collector = BooksCollector()

        if should_be_added:
            collector.add_new_book(book_name)

        initial_favorites = len(collector.get_list_of_favorites_books())
        collector.add_book_in_favorites(book_name)
        final_favorites = len(collector.get_list_of_favorites_books())

        if should_be_added:
            assert final_favorites == initial_favorites + 1
            assert book_name in collector.get_list_of_favorites_books()
        else:
            assert final_favorites == initial_favorites

    def test_delete_book_from_favorites_removes_book(self):
        collector = BooksCollector()
        book_name = "Любимая книга"
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)

        assert book_name in collector.get_list_of_favorites_books()

        collector.delete_book_from_favorites(book_name)
        assert book_name not in collector.get_list_of_favorites_books()

    def test_get_list_of_favorites_books_returns_current_list(self):
        collector = BooksCollector()
        favorite_books = ["Маленький принц", "Гарри Поттер"]

        for book in favorite_books:
            collector.add_new_book(book)
            collector.add_book_in_favorites(book)

        result = collector.get_list_of_favorites_books()
        assert result == favorite_books

    def test_newly_added_book_has_empty_genre(self):
        collector = BooksCollector()
        book_name = "Новая книга"
        collector.add_new_book(book_name)
        genre = collector.get_book_genre(book_name)
        assert genre == ""

    def test_duplicate_book_not_added(self):
        collector = BooksCollector()
        book_name = "Война и мир"
        collector.add_new_book(book_name)
        initial_count = len(collector.get_books_genre())
        collector.add_new_book(book_name)  # попытка добавить дубликат
        final_count = len(collector.get_books_genre())
        assert final_count == initial_count  # количество книг не изменилось
