# Файл: test_books_collector.py (класс + тесты в одном файле)


class BooksCollector:
    def __init__(self):
        self.books_genre = {}
        self.favorites = []
        self.genre = ['Фантастика', 'Ужасы', 'Детективы', 'Мультфильмы', 'Комедии']
        self.genre_age_rating = ['Ужасы', 'Детективы']

    # добавляем новую книгу
    def add_new_book(self, name):
        if not self.books_genre.get(name) and 0 < len(name) < 41:
            self.books_genre[name] = ''

    # устанавливаем книге жанр
    def set_book_genre(self, name, genre):
        if name in self.books_genre and genre in self.genre:
            self.books_genre[name] = genre

    # получаем жанр книги по её имени
    def get_book_genre(self, name):
        return self.books_genre.get(name)

    # выводим список книг с определённым жанром
    def get_books_with_specific_genre(self, genre):
        books_with_specific_genre = []
        if self.books_genre and genre in self.genre:
            for name, book_genre in self.books_genre.items():
                if book_genre == genre:
                    books_with_specific_genre.append(name)
        return books_with_specific_genre

    # получаем словарь books_genre
    def get_books_genre(self):
        return self.books_genre

    # возвращаем книги, подходящие детям
    def get_books_for_children(self):
        books_for_children = []
        for name, genre in self.books_genre.items():
            if genre not in self.genre_age_rating and genre in self.genre:
                books_for_children.append(name)
        return books_for_children

    # добавляем книгу в Избранное
    def add_book_in_favorites(self, name):
        if name in self.books_genre:
            if name not in self.favorites:
                self.favorites.append(name)

    # удаляем книгу из Избранного
    def delete_book_from_favorites(self, name):
        if name in self.favorites:
            self.favorites.remove(name)

    # получаем список Избранных книг
    def get_list_of_favorites_books(self):
        return self.favorites


import unittest
from parameterized import parameterized

class TestBooksCollector(unittest.TestCase):
    def setUp(self):
        """Создаёт новый экземпляр BooksCollector перед каждым тестом"""
        self.collector = BooksCollector()

    @parameterized.expand([
        ("Война и мир", True),  # корректное название
        ("", False),  # пустая строка
        ("a" * 41, False),  # слишком длинное название (>40 символов)
        ("Преступление и наказание", True),  # ещё одно корректное название
        ("Гарри Поттер", True),  # книга с обычным названием
    ])
    def test_add_new_book(self, book_name, should_be_added):
        """Проверяет добавление книг с разными названиями"""
        self.collector.add_new_book(book_name)
        if should_be_added:
            self.assertIn(book_name, self.collector.get_books_genre())
            self.assertEqual(self.collector.get_book_genre(book_name), '')
        else:
            self.assertNotIn(book_name, self.collector.get_books_genre())

    @parameterized.expand([
        ("1984", "Фантастика", True),  # книга есть, жанр допустимый
        ("Мастер и Маргарита", "Ужасы", True),  # книга есть, жанр допустимый
        ("Неизвестная книга", "Фантастика", False),  # книги нет в словаре
        ("Война и мир", "Неизвестный жанр", False),  # недопустимый жанр
    ])
    def test_set_book_genre(self, book_name, genre, should_set):
        """Проверяет установку жанров для разных сценариев"""
        # Предварительно добавляем книгу, если она должна существовать
        if book_name != "Неизвестная книга":
            self.collector.add_new_book(book_name)

        self.collector.set_book_genre(book_name, genre)
        if should_set:
            genre_value = self.collector.get_book_genre(book_name)
        else:
            # Если не должен установиться, проверяем, что жанр остался пустым
            genre_value = self.collector.get_book_genre(book_name)
            self.assertEqual(genre_value, '' if book_name in self.collector.books_genre else None)

    def test_get_book_genre_existing_book(self):
        """Проверяет получение жанра существующей книги"""
        book_name = "Дюна"
        genre = "Фантастика"
        self.collector.add_new_book(book_name)
        self.collector.set_book_genre(book_name, genre)
        result = self.collector.get_book_genre(book_name)
        self.assertEqual(result, genre)

    def test_get_book_genre_nonexistent_book(self):
        """Проверяет получение жанра несуществующей книги"""
        result = self.collector.get_book_genre("Неизвестная книга")
        self.assertIsNone(result)

    @parameterized.expand([
        ("Фантастика", ["Дюна", "451 градус по Фаренгейту"]),  # жанр с книгами
        ("Ужасы", ["Оно"]),  # другой жанр с книгами
        ("Неизвестный жанр", []),  # недопустимый жанр
        ("Комедии", []),  # жанр без книг
    ])
    def test_get_books_with_specific_genre(self, genre, expected_books):
        """Проверяет получение книг определённого жанра"""
        # Добавляем тестовые данные
        test_data = [
            ("Дюна", "Фантастика"),
            ("451 градус по Фаренгейту", "Фантастика"),
            ("Оно", "Ужасы"),
        ]
        for book, book_genre in test_data:
            self.collector.add_new_book(book)
            self.collector.set_book_genre(book, book_genre)

        result = self.collector.get_books_with_specific_genre(genre)
        self.assertEqual(sorted(result), sorted(expected_books))

    def test_get_books_genre(self):
        """Проверяет возврат текущего словаря books_genre"""
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
        self.collector.add_new_book("Шерлок Холмс")
        self.collector.set_book_genre("Шерлок Холмс", "Детективы")  # возрастной рейтинг
        self.collector.add_new_book("Смешарики")
        self.collector.set_book_genre("Смешарики", "Комедии")  # без возрастного рейтинга

        result = self.collector.get_books_for_children()
        # Книги с возрастным рейтингом не должны быть в списке
        self.assertNotIn("Оно", result)
        self.assertNotIn("Шерлок Холмс", result)
        # Книги без возрастного рейтинга должны быть в списке
        self.assertIn("Король Лев", result)
        self.assertIn("Смешарики", result)

    @parameterized.expand([
        ("Гарри Поттер", True),  # книга существует