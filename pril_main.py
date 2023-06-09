import sys
from PyQt6.QtWidgets import QApplication, QComboBox,QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from books import BooksWin
from users import UsersWin
import sqlite3
from datetime import date


# TODO: ПРОБЛЕМЫ с ID при выдаче!!!! отсортировать выпадающие списки по алфавиту. А если убирать выданные книги из списка?

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # создаем соединение с нашей базой данных
        self.conn = sqlite3.connect('library.db')
        self.cur = self.conn.cursor()

        self.conn.commit()

        self.setWindowTitle('БИБЛИОТЕКА')
        self.setGeometry(100, 50, 500, 700)


        # -----------------------------------------кнопки----------------------------------------------

        self.btn_books = QPushButton('КНИГИ', self)
        self.btn_books.setGeometry(10, 20, 235, 200)
        self.btn_books.clicked.connect(self.openBooksWindow)
        self.btn_books.setStyleSheet("QPushButton:hover{border-image: url(lib1.png)}")

        self.btn_users = QPushButton('ЧИТАТЕЛИ', self)
        self.btn_users.setGeometry(255, 20, 235, 200)
        self.btn_users.clicked.connect(self.openUsersWindow)
        self.btn_users.setStyleSheet("QPushButton:hover{border-image: url(users.png)}")
        # кнопка выдачи книг
        self.issue_button = QPushButton('Выдать книгу', self)
        self.issue_button.move(20, 350)
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

        # кнопка возврата книги
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
        self.return_button.move(150, 350)
        self.return_button.clicked.connect(self.return_book)

        # кнопка выданные книги
        self.output_book_button = QPushButton('Выданные книги', self)
        self.output_book_button.setStyleSheet("""
                   QPushButton{
                       font-style: oblique;
                       font-weight: bold;
                       border: 1px solid #1DA1F2;
                       border-radius: 15px;
                       color: #1DA1F2;
                       background-color: #fff;
                   }
                   """)
        self.output_book_button.setGeometry(280, 350, 120, 30)
        self.output_book_button.clicked.connect(self.output_book)


        # -------------------------------------------------виджеты----------------------------------------------
        # создаем текстовый виджет
        self.output = QTextEdit(self)
        self.output.setGeometry(25, 400, 400, 275)

        self.title = QLabel('ВЫДАЧА И ПРИЁМ КНИГ:', self)
        self.title.setGeometry(30, 235, 450, 12)


        self.name_book_label = QLabel('Название книги:', self)
        self.name_book_label.move(20, 260)

        self.name_book_entry = QComboBox(self)
        self.name_book_entry.setGeometry(150,260,200,30)
        # создаём список книг, преобразуя кортедж из поиска в список
        self.item_book = [title[0] for title in self.cur.execute("""SELECT title FROM books""").fetchall()]
        self.name_book_entry.addItems(self.item_book)
        self.name_book_entry.setCurrentIndex(-1)    #очищение поля


        self.name_user_label = QLabel('Имя читателя:', self)
        self.name_user_label.move(20, 300)

        self.name_user_entry = QComboBox(self,)
        self.name_user_entry.setGeometry(150, 300,200,30)
        self.item_user = [name[0] for name in self.cur.execute("""SELECT name FROM users""").fetchall()]
        self.name_user_entry.addItems(self.item_user)
        self.name_user_entry.setCurrentIndex(-1)

        self.show()
    def openBooksWindow(self):
        self.books_window = BooksWin()
        self.books_window.show()

    def openUsersWindow(self):
        self.users_window = UsersWin()
        self.users_window.show()

    # функция выдачи книг
    def issue_book(self):
        name_book = self.name_book_entry.currentText()
        name_user = self.name_user_entry.currentText()
        # проверка на сущетсвование пользователя в БД
        flag = False
        for cur_name_user in self.cur.execute(
                """SELECT name FROM users""").fetchall():  # проходимся циклом по всем пользователям и проверяем
            if cur_name_user[0] == name_user:
                flag = True
        if not flag:
            self.output.clear()
            self.output.append(f"Данного пользователя не существует в базе данных! Добавьте пользователя в базу данных,\
            чтобы выдать книгу!")
            return
        else:
            self.cur.execute('''UPDATE books SET available = 0 
                     WHERE title = ? AND available = 1''', (name_book,))
            # проверка сущетсвования книги в БД
            if self.cur.rowcount == 0:
                self.output.clear()
                self.output.append(f'Этой книги нет в библиотеке! Возьмите другую')
                self.name_book_entry.setCurrentIndex(-1)
                self.name_user_entry.setCurrentIndex(-1)
                return
            self.cur.execute('''INSERT INTO issue_log (name_user, name_book, data) 
                             VALUES (?, ?, ?)''', (name_user, name_book, date.today()))
            self.conn.commit()
            self.output.clear()
            self.output.append(f'Книга успешно выдана')
            self.name_book_entry.setCurrentIndex(-1) #очищение поля
            self.name_user_entry.setCurrentIndex(-1)


    def return_book(self):
        name_book = self.name_book_entry.currentText()
        self.cur.execute('''SELECT * FROM issue_log WHERE name_book = ?''', (name_book,))
        issue = self.cur.fetchone()
        if issue is None:
            self.output.clear()
            self.output.append(f'Книга уже возвращена!')
            self.name_book_entry.setCurrentIndex(-1)
            self.name_user_entry.setCurrentIndex(-1)
            return
        self.cur.execute('''UPDATE books SET available = 1 WHERE title = ?''', (name_book,))
        self.cur.execute('''DELETE FROM issue_log WHERE id = ?''', (issue[0],))
        self.conn.commit()
        self.output.clear()
        self.output.append(f'Книга {name_book} успешно возвращена!')
        self.name_book_entry.setCurrentIndex(-1)
        self.name_user_entry.setCurrentIndex(-1)


    def output_book(self):
        self.cur.execute("SELECT * FROM issue_log")
        books = self.cur.fetchall()
        if books is None:  #TODO: даже если все книги возвращены - всё равно не выводит эту надпись
            self.output.clear()
            self.output.append(f"Все книги возвращены")
        for cur_book in books:
            self.output.append(f'id читателя-{cur_book[0]}, {cur_book[1]}, {cur_book[2]}, {cur_book[3]}')  #tODO: неправильно выводятся индексы!!!
<<<<<<< HEAD
                                                                                                        #todo: id продолжают увеличиваться, даже если возвращаешь книгу
        self.name_book_entry.setCurrentIndex(-1)  # очищение поля                                    #todo: может вообще убрать эти id в базе данных выдачи
                                                                                                #todo: они функционала никакого не имеют
=======

        self.name_book_entry.setCurrentIndex(-1)  # очищение поля
>>>>>>> 2a0bb05877c6b50bcc3aedc62478f900b733101a
        self.name_user_entry.setCurrentIndex(-1)

    def closeEvent(self, event):
        # закрываем соединение с базой данных при закрытии приложения
        self.conn.close()


if __name__ == '__main__':
    app = QApplication(
        sys.argv)  # создаем экзэмпляр класса. аргументы sys.argv используются для инициализации QApplication

    main_window = MainWindow()
    #main_window.setStyleSheet("QLineEdit { background-color: yellow }")
    main_window.show()
    sys.exit(app.exec())  # sys.exit() гарантирует, что приложение завершится
    # корректно при завершении цикла обработки событий(app.exec_()).
