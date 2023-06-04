import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtGui import QFont
import sqlite3
from datetime import date


class LibraryApp(QMainWindow):

    def __init__(self):
        super().__init__()

        # создаем соединение с нашей базой данных
        self.conn = sqlite3.connect('library.db')
        self.cur = self.conn.cursor()

        self.conn.commit()

        # создаем графический интерфейс
        self.setWindowTitle('Библиотека')
        self.setGeometry(50, 50, 800, 800)

        # создаем виджеты для ввода данных
        self.title_label = QLabel('Название книги:', self)
        self.title_label.move(20, 20)
        self.title_label.setFont(QFont("Times", 8, QFont.Bold))
        self.title_entry = QLineEdit(self, placeholderText='title')
        self.title_entry.move(150, 20)

        self.author_label = QLabel('Автор книги:', self)
        self.author_label.move(20, 60)
        self.author_label.setFont(QFont("Times", 8, QFont.Bold))
        self.author_entry = QLineEdit(self, placeholderText='author')
        self.author_entry.move(150, 60)

        self.genre_label = QLabel('Жанр книги:', self)
        self.genre_label.move(20, 100)
        self.genre_label.setFont(QFont("Times", 8, QFont.Bold))
        self.genre_entry = QLineEdit(self, placeholderText='genre')
        self.genre_entry.move(150, 100)

        self.year_label = QLabel('Год издания:', self)
        self.year_label.move(20, 140)
        self.year_label.setFont(QFont("Times", 8, QFont.Bold))
        self.year_entry = QLineEdit(self, placeholderText='year')
        self.year_entry.move(150, 140)

        # создаем кнопки для добавления и вывода книг
        self.add_button = QPushButton('Добавить книгу', self)
        self.add_button.move(20, 180)
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

        #кнопка выдачи книг
        self.issue_button = QPushButton('Выдать книгу', self)
        self.issue_button.move(400, 350)
        self.issue_button.setStyleSheet("""
        QPushButton{
            font-style: oblique;
            font-weight: bold;
            border: 1px solid #1DA1F2;
            border-radius: 15px;
            color: #1DA1F2;
            background-color: #fff;
        }
        """)
        self.issue_button.clicked.connect(self.issue_book)

        #кнопка возврата книги
        self.return_button = QPushButton('Вернуть книгу', self)
        self.return_button.setStyleSheet("""
                QPushButton{
                    font-style: oblique;
                    font-weight: bold;
                    border: 1px solid #1DA1F2;
                    border-radius: 15px;
                    color: #1DA1F2;
                    background-color: #fff;
                }
                """)
        self.return_button.move(510, 350)
        self.return_button.clicked.connect(self.return_book)

        # создаем текстовый виджет для вывода списка книг
        self.output = QTextEdit(self)
        self.output.setGeometry(20, 220, 360, 350)

        #загаловок
        self.label = QLabel('Выдача и возврат книг', self)
        self.label.setGeometry(400, 220, 150, 30)
        self.label.move(400, 220)
        self.label.setFont(QFont("Times", 8, QFont.Bold))

        self.name_book_label = QLabel('Название книги:', self)
        self.name_book_label.move(400, 250)
        self.name_book_label.setFont(QFont("Times", 8, QFont.Bold))
        self.name_book_entry = QLineEdit(self, placeholderText='title')
        self.name_book_entry.move(500, 250)

        self.name_user_label = QLabel('Имя читателя:', self)
        self.name_user_label.move(400, 300)
        self.name_user_label.setFont(QFont("Times", 8, QFont.Bold))
        self.name_user_entry = QLineEdit(self, placeholderText='users(name)')
        self.name_user_entry.move(500, 300)




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
        #очищаем поля ввода!!!!!
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
    #функция выдачи книг
    def issue_book(self):
        name_book = self.name_book_entry.text()
        name_user = self.name_user_entry.text()
        #проверка на сущетсвование пользователя в БД
        if self.cur.execute("""SELECT name FROM users""").fetchall() != name_user:
            self.output.clear()
            self.output.append(f"Данного пользователя не существует в базе данных! Добавьте пользователя в базу данных,\
            чтобы выдать книгу!")
            return
        else:
            self.cur.execute('''UPDATE books SET available = 0 
                     WHERE title = ? AND available = 1''', (name_book,))
            #проверка сущетсвования книги в БД
            if self.cur.rowcount == 0:
                self.output.clear()
                self.output.append(f'Этой книги к сожаление нет в библиотеки! Возьмите другую')
                return
            self.cur.execute('''INSERT INTO issue_log (name_user, name_book, data) 
                             VALUES (?, ?, ?)''', (name_user, name_book, date.today()))
            self.conn.commit()
            self.output.clear()
            self.output.append(f'Книга успешно выдана')


    def return_book(self):
        name_book = self.name_book_entry.text()
        self.cur.execute('''SELECT * FROM issue_log WHERE name_book = ?''', (name_book,))
        issue = self.cur.fetchone()
        if issue is None:
            self.output.clear()
            self.output.append(f'Книга уже возвращена!')
            return
        self.cur.execute('''UPDATE books SET available = 1 WHERE title = ?''', (name_book,))
        self.cur.execute('''DELETE FROM issue_log WHERE id = ?''', (issue[0],))
        self.conn.commit()
        self.output.clear()
        self.output.append(f'Книга {name_book} успешно возвращена!')

    def closeEvent(self, event):
        # закрываем соединение с базой данных при закрытии приложения
        self.conn.close()



if __name__ == '__main__':
    app = QApplication(
        sys.argv)  # создаем экзэмпляр класса. аргументы sys.argv используются для инициализации QApplication
    library_app = LibraryApp()  # создаем обьект класс
    library_app.show()  # выводим его на экран
    sys.exit(app.exec_())  # sys.exit() гарантирует, что приложение завершится
    # корректно при завершении цикла обработки событий(app.exec_()).
