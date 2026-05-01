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

    @parameterized.expand([
        ("1984", "Фантастика", True),  # книга есть, жанр допустимый
        ("Мастер и Маргарита", "Неизвестный жанр", False),  # недопустимый жанр
        ("Неизвестная книга", "Фантастика", False),  # книги нет в словаре
    ])
    def test_set_book_genre(self, book_name, genre, should_set):
        """Проверяет установку жанров для разных сценариев"""
        # Предварительно добавляем книгу, если она должна существовать
        if book_name != "Неизвестная книга":
            self.collector.add_new_book(book_name)

        self.collector.set_book_genre(book_name, genre)
        if should_set:
            self.assertEqual(self.collector.get_book_genre(book_name), genre)
        else:
            # Если не должен установиться, проверяем, что либо None, либо пустая строка
            genre_value = self.collector.get_book_genre(book_name)
            self.assertTrue(genre_value is None or genre_value == "")

    @parameterized.expand([
        ("Гарри Поттер", "Фэнтези"),  # книга с жанром
        ("Неизвестная книга", None),  # несуществующая книга
    ])
    def test_get_book_genre(self, book_name, expected_genre):
        """Проверяет получение жанра книги"""
        if book_name == "Гарри Поттер":
            self.collector.add_new_book(book_name)
            self.collector.set_book_genre(book_name, "Фэнтези")

        result = self.collector.get_book_genre(book_name)
        self.assertEqual(result, expected_genre)

    @parameterized.expand([
        ("Фантастика", ["Дюна", "451 градус по Фаренгейту"]),  # жанр с книгами
        ("Неизвестный жанр", []),  # недопустимый жанр
    ])
    def test_get_books_with_specific_genre(self, genre, expected_books):
        """Проверяет получение книг определённого жанра"""
        # Добавляем тестовые данные
        if genre == "Фантастика":
            self.collector.add_new_book("Дюна")
            self.collector.set_book_genre("Дюна", "Фантастика")
            self.collector.add_new_book("451 градус по Фаренгейту")
            self.collector.set_book_genre("451 градус по Фаренгейту", "Фантастика")

        result = self.collector.get_books_with_specific_genre(genre)
        self.assertEqual(sorted(result), sorted(expected_books))

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

        result = self.collector.get_books_for_children()
        # "Оно" не должно быть в списке, "Король Лев" должен быть
        self.assertNotIn("Оно", result)
        self.assertIn("Король Лев", result)

    @parameterized.expand([
        ("Гарри Поттер", True),  # книга существует
        ("Неизвестная книга", False),  # книги нет в словаре
        ("Гарри Поттер", False),  # дубликат (добавляем дважды)
    ])
    def test_add_book_in_favorites(self, book_name, should_add):
        """Проверяет добавление книги в избранное"""
        # Предварительно добавляем книгу
        if book_name != "Неизвестная книга":
            self.collector.add_new_book(book_name)

        # Если это дубликат, сначала добавляем один раз
        if not should_add:
            self.collector.add_book_in_favorites(book_name)

        initial_count = len(self.collector.get_list_of_favorites_books())
        self.collector.add_book_in_favorites(book_name)
        final_count = len(self.collector.get_list_of_favorites_books())

        if should_add:
            self.assertEqual(final_count, initial_count + 1)
        else:
            self.assertEqual(final_count, initial_count)

    def test_delete_book_from_favorites(self):
        """Проверяет удаление книги из избранного"""
        # Добавляем книгу в избранное
        self.collector.add_new_book("Убить пересмешника")
        self.collector.add_book_in_favorites("Убить пересмешника")

        # Удаляем
        self.collector.delete_book_from_favorites("Убить пересмешника")
        result = self.collector.get_list_of_favorites_books()
        self.assertNotIn("Убить пересмешника", result)

    def test_get_list_of_favorites_books(self):
        """Проверяет получение списка избранных книг"""
        # Добавляем несколько книг в избранное
        books_to_add = ["1984", "О дивный новый мир", "Скотный двор"]
        for book in books_to_add:
            self.collector.add_new_book(book)
            self.collector.add_book_in_favorites(book)

        result = self.collector.get_list_of_favorites_books()
        self.assertEqual(sorted(result), sorted(books_to_add))
