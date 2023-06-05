import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit
import sqlite3
from PyQt6.QtGui import QPalette, QPixmap
from PyQt5.QtCore import Qt

class BooksWin(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QWidget {
                background-color: #333333;
                color: #ffffff;
            }
            QPushButton {
                background-color: #555555;
                color: #ffffff;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QLineEdit {
                background-color: #444444;
                color: #ffffff;
            }
        """)


        # создаем соединение с нашей базой данных
        self.conn = sqlite3.connect('library.db')
        self.cur = self.conn.cursor()

        self.conn.commit()

        # создаем графический интерфейс
        self.setWindowTitle('Библиотека')

        self.setGeometry(100, 100, 500, 500)

        # создаем виджеты для ввода данных
        self.title_label = QLabel('Название книги:', self)
        self.title_label.move(20, 20)

        self.title_entry = QLineEdit(self, placeholderText='title')
        self.title_entry.move(150, 20)

        self.author_label = QLabel('Автор книги:', self)
        self.author_label.move(20, 60)

        self.author_entry = QLineEdit(self, placeholderText='author')
        self.author_entry.move(150, 60)

        self.genre_label = QLabel('Жанр книги:', self)
        self.genre_label.move(20, 100)

        self.genre_entry = QLineEdit(self, placeholderText='genre')
        self.genre_entry.move(150, 100)

        self.year_label = QLabel('Год издания:', self)
        self.year_label.move(20, 140)

        self.year_entry = QLineEdit(self, placeholderText='year')
        self.year_entry.move(150, 140)

        # создаем кнопки для добавления и вывода книг
        self.add_button = QPushButton('Добавить книгу', self)
        self.add_button.move(20, 180)
        self.add_button.setGeometry(20, 180, 120, 30)
        self.add_button.setStyleSheet('background: rgb(255,0,0);')
        self.add_button.setStyleSheet("""
        QPushButton{
            font-style: oblique;
            font-weight: bold;
            border: 1px solid #1DA1F2;
            border-radius: 15px;
            color: #1DA1F2;
            background-color: #fff;
        }
        """)
        self.add_button.clicked.connect(self.add_book)

        self.show_button = QPushButton('Показать книги', self)
        self.show_button.move(150, 180)
        self.show_button.setGeometry(150, 180, 120, 30)
        self.show_button.setStyleSheet("""
        QPushButton{
            font-style: oblique;
            font-weight: bold;
            border: 1px solid #1DA1F2;
            border-radius: 15px;
            color: #1DA1F2;
            background-color: #fff;
        }
        """)
        self.show_button.clicked.connect(self.show_books)


        # создаем текстовый виджет для вывода списка книг
        self.output = QTextEdit(self)
        self.output.setGeometry(20, 220, 420, 250)


    # функция для добавления книги в базу данных
    def add_book(self):
        # получаем данные из полей ввода
        title = self.title_entry.text()
        author = self.author_entry.text()
        year = self.year_entry.text()
        genre = self.genre_entry.text()
        # добавляем книгу в базу данных
        self.cur.execute('INSERT OR REPLACE INTO books (title, author, genre, year) VALUES (?, ?, ?, ?)',
                         (title, author, genre, year))
        self.conn.commit()
        # очищаем поля ввода!!!!!
        self.title_entry.setText('')
        self.author_entry.setText('')
        self.year_entry.setText('')
        self.genre_entry.setText('')

    # функция для вывода списка книг из базы данных
    def show_books(self):
        # получаем все книги из базы данных
        self.cur.execute('SELECT * FROM books')
        books = self.cur.fetchall()
        # print(books)
        # очищаем текстовый виджет
        self.output.clear()
        # выводим список книг в текстовый виджет
        for book in books:
            self.output.append(f'{book[0]}.  {book[1]}, {book[2]}, {book[3]}, {book[4]}, {book[5]}')


    def closeEvent(self, event):
        # закрываем соединение с базой данных при закрытии приложения
        self.conn.close()

stylesheet = """
    BooksWin {
        background-image: url("D:\imag\lib.jpg"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
"""

if __name__ == '__main__':
    app = QApplication(
        sys.argv)  # создаем экзэмпляр класса. аргументы sys.argv используются для инициализации QApplication
    book_win = BooksWin()  # создаем обьект класс
    app.setStyleSheet(stylesheet)

    book_win.show()  # выводим его на экран
    sys.exit(app.exec())  # sys.exit() гарантирует, что приложение завершится
    # корректно при завершении цикла обработки событий(app.exec_()).
