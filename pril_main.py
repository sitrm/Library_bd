import sys
from PyQt6.QtWidgets import QApplication, QComboBox,QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout
from books import BooksWin
from users import UsersWin
import sqlite3
from datetime import date


#todo: сломал выдачу книг, добавив людей с одинаковыми фио
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
        self.name_book_entry.setGeometry(150, 260, 200, 30)
        # создаём список книг, преобразуя кортедж из поиска в список
        self.item_book = [title[0] for title in self.cur.execute("""SELECT title FROM books""").fetchall()]
        self.name_book_entry.addItems(self.item_book)
        self.name_book_entry.setCurrentIndex(-1)    #очищение поля


        self.name_user_label = QLabel('Имя читателя:', self)
        self.name_user_label.move(20, 300)

        self.name_user_entry = QComboBox(self,)
        self.name_user_entry.setGeometry(150, 300, 200, 30)
        self.item_user_id = [cur_id[0] for cur_id in self.cur.execute("""SELECT user_id FROM users""").fetchall()]
        self.item_user_name = [self.cur.execute("SELECT name FROM users WHERE user_id = ?", (cur_id[0],)).fetchall()[0][0] for
                          cur_id in self.cur.execute("""SELECT user_id FROM users""").fetchall()]
        self.arr_id_name = []
        for id_, name in zip(list(map(str, self.item_user_id)), self.item_user_name):
            self.arr_id_name.append(f'id-{id_} , {name}')
        self.name_user_entry.addItems(self.arr_id_name)
        self.name_user_entry.setCurrentIndex(-1)

        self.show()

#-----------------------------------------------------------функции----------------------------------------------------------------------------
    def openBooksWindow(self):
        self.books_window = BooksWin()
        self.books_window.show()

    def openUsersWindow(self):
        self.users_window = UsersWin()
        self.users_window.show()

    # функция выдачи книг
<<<<<<< HEAD
    def issue_book(self):
        name_book = self.name_book_entry.currentText() #TODO: починил. Проблема была в том, что в user_id мы передевали f-строку. 
        user_id = self.name_user_entry.currentText()[3] + self.name_user_entry.currentText()[4]
=======
    def issue_book(self):   #todo: НЕ РАБОТАЕТ
        name_book = self.name_book_entry.currentText() #todo: если будет время - сделать, чтобы выданные книги исчезали из выпадающего списка. ну ил пофииг
        user_id = self.name_user_entry.currentText()
        print(user_id)
>>>>>>> cf6f64eb306c037c9bd82e756eab112a3ef2476f

        self.cur.execute('''UPDATE books SET available = 0 WHERE title = ? AND available = 1''', (name_book,))
        # проверка сущетсвования книги в БД
        if self.cur.rowcount == 0:
            self.output.clear()
            self.output.append(f'Этой книги нет в библиотеке! Возьмите другую.')
            self.name_book_entry.setCurrentIndex(-1)
            self.name_user_entry.setCurrentIndex(-1)

        name_user = self.cur.execute("SELECT name FROM users WHERE user_id = ?", (int(user_id),)).fetchall()
<<<<<<< HEAD

=======
        #не доходит до сюда
        print(name_user)
>>>>>>> cf6f64eb306c037c9bd82e756eab112a3ef2476f
        self.cur.execute('''INSERT INTO issue_log (user_id, name_user, name_book, data) VALUES (?, ?, ?, ?)''', (user_id, name_user[0][0], name_book, date.today()))
        self.conn.commit()
        self.output.clear()
        self.output.append(f'Книга {name_book} успешно выдана!')
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
        self.output.clear()  #чистим логи
        check = self.cur.execute("SELECT COUNT(*) FROM issue_log").fetchall()[0][0]
        if check == 0:
            self.output.clear()
            return self.output.append(f"Все книги возвращены!")
        books = self.cur.execute("SELECT * FROM issue_log").fetchall()
        i = 1
        for cur_book in books:
            self.output.append(f'{i}) {cur_book[2]} id - {cur_book[1]}, {cur_book[3]}, {cur_book[4]}')
            i += 1

        self.name_book_entry.setCurrentIndex(-1)  # очищение поля
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
