import unittest
from parameterized import parameterized
from books_collector import BooksCollector

class TestBooksCollector(unittest.TestCase):
    def setUp(self):
        """Создаёт новый экземпляр BooksCollector перед каждым тестом"""
        self.collector = BooksCollector()

    @parameterized.expand([
        ("Война и мир", True),  # корректное название
        ("", False),  # пустая строка
        ("a" * 41, False),  # слишком длинное название (>40 символов)
        ("Преступление и наказание", True),  # ещё одно корректное название
    ])
    def test_add_new_book(self, book_name, should_be_added):
        """Проверяет добавление книг с разными названиями"""
        self.collector.add_new_book(book_name)
        if should_be_added:
            self.assertIn(book_name, self.collector.get_books_genre())
        else:
            self.assertNotIn(book_name, self.collector.get_books_genre())

    def test_set_book_genre_valid_book_and_genre(self):
        """Проверяет установку жанра для существующей книги с допустимым жанром"""
        book_name = "1984"
        genre = "Фантастика"
        self.collector.add_new_book(book_name)
        self.collector.set_book_genre(book_name, genre)
        self.assertEqual(self.collector.get_book_genre(book_name), genre)

    def test_set_book_genre_invalid_genre(self):
        """Проверяет, что жанр не устанавливается для недопустимого жанра"""
        book_name = "Мастер и Маргарита"
        invalid_genre = "Неизвестный жанр"
        self.collector.add_new_book(book_name)
        self.collector.set_book_genre(book_name, invalid_genre)
        # Проверяем, что жанр остался None или пустой строкой
        genre_value = self.collector.get_book_genre(book_name)
        self.assertTrue(genre_value is None or genre_value == "")

    def test_set_book_genre_nonexistent_book(self):
        """Проверяет, что нельзя установить жанр для несуществующей книги"""
        book_name = "Неизвестная книга"
        genre = "Фантастика"
        self.collector.set_book_genre(book_name, genre)
        # Книга не должна появиться в словаре
        self.assertNotIn(book_name, self.collector.get_books_genre())

    def test_get_book_genre_existing_book(self):
        """Проверяет получение жанра для существующей книги через прямой доступ к словарю"""
        book_name = "Гарри Поттер"
        expected_genre = "Фэнтези"
        # Добавляем книгу и устанавливаем жанр
        self.collector.add_new_book(book_name)
        self.collector.set_book_genre(book_name, expected_genre)
        # Получаем жанр через словарь
        books_genre = self.collector.get_books_genre()
        self.assertEqual(books_genre.get(book_name), expected_genre)

    def test_get_book_genre_nonexistent_book(self):
        """Проверяет получение жанра для несуществующей книги"""
        book_name = "Неизвестная книга"
        result = self.collector.get_book_genre(book_name)
        self.assertIsNone(result)

    def test_get_books_with_specific_genre_existing_genre(self):
        """Проверяет получение книг определённого жанра с разнообразными тестовыми данными"""
        # Добавляем книги разных жанров
        self.collector.add_new_book("Дюна")
        self.collector.set_book_genre("Дюна", "Фантастика")
        self.collector.add_new_book("451 градус по Фаренгейту")
        self.collector.set_book_genre("451 градус по Фаренгейту", "Фантастика")
        self.collector.add_new_book("Анна Каренина")
        self.collector.set_book_genre("Анна Каренина", "Классика")
        # Получаем книги жанра "Фантастика"
        result = self.collector.get_books_with_specific_genre("Фантастика")
        expected = ["Дюна", "451 градус по Фаренгейту"]
        self.assertEqual(sorted(result), sorted(expected))

    def test_get_books_with_specific_genre_nonexistent_genre(self):
        """Проверяет получение книг для несуществующего жанра"""
        result = self.collector.get_books_with_specific_genre("Неизвестный жанр")
        self.assertEqual(result, [])

    def test_get_books_genre(self):
        """Проверяет возврат текущего словаря книг и жанров"""
        expected = {"Война и мир": "Классика"}
        self.collector.add_new_book("Война и мир")
        self.collector.set_book_genre("Война и мир", "Классика")
        result = self.collector.get_books_genre()
        self.assertEqual(result, expected)

    def test_get_books_for_children(self):
        """Проверяет, что книги с возрастным рейтингом отсутствуют в списке для детей"""
        # Добавляем книги разных жанров
        self.collector.add_new_book("Оно")
        self.collector.set_book_genre("Оно", "Ужасы")  # возрастной рейтинг
        self.collector.add_new_book("Король Лев")
        self.collector.set_book_genre("Король Лев", "Мультфильмы")  # без возрастного рейтинга
        # Получаем список книг для детей
        result = self.collector.get_books_for_children()
        # Ожидаем только "Король Лев"
        expected = ["Король Лев"]
        self.assertEqual(sorted(result), sorted(expected))

    def test_add_book_in_favorites_existing_book(self):
        """Проверяет добавление существующей книги в избранное"""
        book_name = "Гарри Поттер"
        self.collector.add_new_book(book_name)
        initial_count = len(self.collector.get_list_of_favorites_books())
        self.collector.add_book_in_favorites(book_name)
        final_count = len(self.collector.get_list_of_favorites_books())
        self.assertEqual(final_count, initial_count + 1)

    def test_add_book_in_favorites_nonexistent_book(self):
        """Проверяет, что нельзя добавить несуществующую книгу в избранное"""
        book_name = "Неизвестная книга"
        initial_count = len(self.collector.get_list_of_favorites_books())
        self.collector.add_book_in_favorites(book_name)
        final_count = len(self.collector.get_list_of_favorites_books())
        self.assertEqual(final_count, initial_count)

    def test_add_book_in_favorites_duplicate(self):
        """Проверяет, что дубликат книги не добавляется в избранное"""
        book_name = "Гарри Поттер"
        self.collector.add_new_book(book_name)
        # Сначала добавляем один раз
        self.collector.add_book_in_favorites(book_name)
        initial_count = len(self.collector.get_list_of_favorites_books())
        # Пытаемся добавить второй раз
        self.collector.add