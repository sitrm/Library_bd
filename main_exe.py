import sys
from PyQt6.QtWidgets import QApplication, QComboBox,QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QCheckBox, QVBoxLayout
import sqlite3
from datetime import date





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
        self.init_books_qb()   #todo добавил функции переинициализации. они вызываются при создании окна, а также при
        #использовании методов добавления и удаления читатаеля и книги


        self.name_user_label = QLabel('Имя читателя:', self)
        self.name_user_label.move(20, 300)

        self.name_user_entry = QComboBox(self,)
        self.name_user_entry.setGeometry(150, 300, 200, 30)
        self.init_users_qb()


        self.show()

#-----------------------------------------------------------функции----------------------------------------------------------------------------
    def init_users_qb(self):
        self.name_user_entry.clear()
        self.item_user_id = [cur_id[0] for cur_id in self.cur.execute("""SELECT user_id FROM users""").fetchall()]
        self.item_user_name = [
            self.cur.execute("SELECT name FROM users WHERE user_id = ?", (cur_id[0],)).fetchall()[0][0] for
            cur_id in self.cur.execute("""SELECT user_id FROM users""").fetchall()]
        self.arr_id_name = []
        for id_, name in zip(list(map(str, self.item_user_id)), self.item_user_name):
            self.arr_id_name.append(f'id-{id_} , {name}')
        self.name_user_entry.addItems(self.arr_id_name)
        self.name_user_entry.setCurrentIndex(-1)

    def init_books_qb(self):
        self.name_book_entry.clear()
        # создаём список книг, преобразуя кортедж из поиска в список
        self.item_book = [title[0] for title in self.cur.execute("""SELECT title FROM books""").fetchall()]
        self.name_book_entry.addItems(self.item_book)
        self.name_book_entry.setCurrentIndex(-1)  # очищение поля

    def openBooksWindow(self):
        self.books_window = BooksWin()
        self.books_window.show()

    def openUsersWindow(self):
        self.users_window = UsersWin()
        self.users_window.show()

    # функция выдачи книг
    def issue_book(self):
        name_book = self.name_book_entry.currentText() #TODO: починил. Проблема была в том, что в user_id мы передевали f-строку.
        user_id = self.name_user_entry.currentText()
        user_id = user_id[3:user_id.find(',', 2)]
        if name_book == '':
            self.output.clear()
            return self.output.append(f'Выберите книгу!')
        if user_id == '':
            self.output.clear()
            return self.output.append(f'Для выдачи книги необходимо указать читателя! Укажите читателя!')

        self.cur.execute('''UPDATE books SET available = 0 WHERE title = ? AND available = 1''', (name_book,))
        # проверка сущетсвования книги в БД
        print(str(self.cur.rowcount))
        if self.cur.rowcount == 0:
            self.output.clear()
            print('hi')
            self.name_book_entry.setCurrentIndex(-1)
            self.name_user_entry.setCurrentIndex(-1)
            return self.output.append(f'Этой книги нет в библиотеке! Возьмите другую.') #todo здесьретёрна не хватало - исправил



        name_user = self.cur.execute("SELECT name FROM users WHERE user_id = ?", (int(user_id),)).fetchall()

        self.cur.execute('''INSERT INTO issue_log (user_id, name_user, name_book, data) VALUES (?, ?, ?, ?)''', (user_id, name_user[0][0], name_book, date.today()))
        self.conn.commit()
        self.output.clear()
        self.output.append(f'Книга {name_book} успешно выдана!')
        self.name_book_entry.setCurrentIndex(-1) #очищение поля
        self.name_user_entry.setCurrentIndex(-1)


    def return_book(self):
        name_book = self.name_book_entry.currentText()
        if name_book == '':
            self.output.clear()
            return self.output.append('Выберите книгу, которую хотите вернуть!')
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

        self.setGeometry(100, 100, 700, 500)
        self.title_sort = QLabel("Сортировать:", self)
        self.title_sort.move(300, 20)
#----------------------------------------------------------------chexboxes-----------------------------------------------
        self.checkbox_issue = QCheckBox('В наличии', self)
        self.checkbox_issue.setGeometry(300, 110, 150, 20)
        self.checkbox_issue.setChecked(False)

        self.checkbox_asc_book = QCheckBox("по названию", self)
        self.checkbox_asc_book.setGeometry(300, 50, 150, 20)
        self.checkbox_asc_book.setChecked(False)

        self.checkbox_asc_author = QCheckBox('по фамилии автора', self)
        self.checkbox_asc_author.setGeometry(300, 70, 150, 20)
        self.checkbox_asc_author.setChecked(False)

        self.checkbox_desc_year = QCheckBox('по году издания', self)
        self.checkbox_desc_year.setGeometry(300, 90, 180, 20)
        self.checkbox_desc_year.setChecked(False)

        # Соединяем сигналы от checkbox с функцией-обработчиком  #TODO: сделал взаимоисключающие сигналы
        self.checkbox_issue.stateChanged.connect(lambda state: self.checkboxStateChanged1(state))
        self.checkbox_asc_author.stateChanged.connect(lambda state: self.checkboxStateChanged2(state))
        self.checkbox_asc_book.stateChanged.connect(lambda state: self.checkboxStateChanged3(state))
        self.checkbox_desc_year.stateChanged.connect(lambda state: self.checkboxStateChanged4(state))

#-----------------------------------------------------------------------------widgets---------------------------------------------------
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
#----------------------------------------------------------------------------buttons--------------------------------------------
        # создаем кнопки для добавления/удаления и вывода книг
        self.add_button = QPushButton('Добавить книгу', self)
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
        self.show_button.setGeometry(300, 130, 120, 30)
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

        self.delete_button = QPushButton('Удалить книгу', self)
        self.delete_button.setGeometry(200, 180, 120, 30)
        self.delete_button.setStyleSheet("""
        QPushButton{
            font-style: oblique;
            font-weight: bold;
            border: 1px solid #1DA1F2;
            border-radius: 15px;
            color: #1DA1F2;
            background-color: #fff;
        }
        """)
        self.delete_button.clicked.connect(self.delete_book)
        self.delete_entry = QLineEdit(self, placeholderText='id книги')
        self.delete_entry.move(325, 180)

        # создаем текстовый виджет для вывода списка книг
        self.output = QTextEdit(self)
        self.output.setGeometry(20, 220, 420, 250)

#-----------------------------------------------------------------------------functions-----------------------------------------------------------

    # функция для добавления книги в базу данных
    def add_book(self):
        # получаем данные из полей ввода
        title = self.title_entry.text()
        author = self.author_entry.text()
        year = self.year_entry.text()
        genre = self.genre_entry.text()

        #----------ПРОВЕРКИ---------------
        if len(author) == 0:
            self.output.clear()
            return self.output.append('Введите автора книги!')
        if len(title) == 0:
            self.output.clear()
            return self.output.append(f'Введите название книги!')
        if len(year) == 0:
            self.output.clear()
            return self.output.append(f'Введите год книги!')
        if len(genre) == 0:
            self.output.clear()
            return self.output.append(f'Введите жанр книги!')
        if not year.isdigit():
            self.output.clear()
            return self.output.append(f'Введите корректно год издания книги!')
        # добавляем книгу в базу данных
        self.cur.execute('INSERT OR REPLACE INTO books (title, author, genre, year, available) VALUES (?, ?, ?, ?, ?)',
                         (title, author, genre, year, 1))
        self.conn.commit()

        main_window.init_books_qb()
        # очищаем поля ввода!!!!!
        self.title_entry.setText('')
        self.author_entry.setText('')
        self.year_entry.setText('')
        self.genre_entry.setText('')

        self.output.clear()
        self.output.append(f'Книга "{title}" успешно добавлена!')

    # функция для вывода списка книг из базы данных
    def show_books(self):
        if self.checkbox_asc_book.isChecked():
            self.cur.execute('SELECT * FROM books ORDER BY title ASC')
            books = self.cur.fetchall()
        elif self.checkbox_asc_author.isChecked():
            # self.cur.execute('SELECT * FROM books ORDER BY author ASC')
            # books = self.cur.fetchall()
            self.cur.execute('SELECT * FROM books ORDER BY SUBSTR(author, INSTR(author, " ") + 1)')

            # я этот грёбанный запрос формировал час. -ооо прикольно не знал такого!
            # я этот грёбанный запрос формировал час
            books = self.cur.fetchall()

        elif self.checkbox_desc_year.isChecked():
            self.cur.execute('SELECT * FROM books ORDER BY year DESC')
            books = self.cur.fetchall()
        elif self.checkbox_issue.isChecked():
            self.cur.execute("SELECT * FROM books WHERE available = 1")
            books = self.cur.fetchall()
        else:
            # получаем все книги из базы данных
            self.cur.execute('SELECT * FROM books')
            books = self.cur.fetchall()

        # очищаем текстовый виджет
        self.output.clear()
        # выводим список книг в текстовый виджет
        i = 1
        for book in books:
            if book[5] == 1:
                issue = 'в наличии'
            else:
                issue = 'выдана'
            self.output.append(f'{i}) {book[1]}, {book[2]}, {book[3]}, {book[4]}, id-{book[0]}. {issue}')
            i += 1

    def delete_book(self):
        book_id = self.delete_entry.text()
        if not book_id.isnumeric():
            self.output.clear()
            return self.output.append(f'ID книги введено не корректно! Введите целое число!')

        flag = False
        for cur_book_id in self.cur.execute('SELECT book_id FROM books').fetchall():
            if str(cur_book_id[0]) == book_id:#str бл!!!!!
                flag = True
        if not flag:
            self.output.clear()
            return self.output.append(f"Книги с id - {book_id} не сущетсвует!")
        else:
            name_book = self.cur.execute('SELECT title FROM books WHERE book_id = ?', (book_id,)).fetchall()[0][0]
            self.cur.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
            self.conn.commit()
            self.delete_entry.setText('')
            self.output.clear()
            self.output.append(f"Книга {name_book} успешно удален!")
        main_window.init_books_qb()
    # self.checkbox_issue.stateChanged.connect(lambda state: self.checkboxStateChanged1(state))
    # self.checkbox_asc_author.stateChanged.connect(lambda state: self.checkboxStateChanged2(state))
    # self.checkbox_asc_book.stateChanged.connect(lambda state: self.checkboxStateChanged3(state))
    # self.checkbox_desc_year.stateChanged.connect(lambda state: self.checkboxStateChanged4(state))
    def checkboxStateChanged1(self,state):
        if state == 2:
            self.checkbox_asc_author.setChecked(False)
            self.checkbox_asc_book.setChecked(False)
            self.checkbox_desc_year.setChecked(False)
    def checkboxStateChanged2(self, state):
        if state == 2:
            self.checkbox_issue.setChecked(False)
            self.checkbox_asc_book.setChecked(False)
            self.checkbox_desc_year.setChecked(False)

    def checkboxStateChanged3(self, state):
        if state == 2:
            self.checkbox_issue.setChecked(False)
            self.checkbox_asc_author.setChecked(False)
            self.checkbox_desc_year.setChecked(False)

    def checkboxStateChanged4(self, state):
        if state == 2:
            self.checkbox_issue.setChecked(False)
            self.checkbox_asc_author.setChecked(False)
            self.checkbox_asc_book.setChecked(False)

    def closeEvent(self, event):
        # закрываем соединение с базой данных при закрытии приложения
        self.conn.close()

class UsersWin(QMainWindow):

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
        self.setWindowTitle('Пользователи')
        self.setGeometry(100, 100, 800, 600)  #position: x,y len: x,y

        # -----------------------------------------виджеты------------------------------------------
        self.name_label = QLabel('ФИ(Иванов И):', self)
        self.name_label.move(20, 100)
        self.name_entry = QLineEdit(self, placeholderText='name')
        self.name_entry.move(150, 100)


        self.rang_label = QLabel('Ранг читателя:', self)  # TODO: auto rang
        self.rang_label.move(20, 140)
        self.rang_entry = QLineEdit(self, placeholderText='rank')
        self.rang_entry.move(150, 140)

        self.phone_label = QLabel('Номер телефона:', self)  # TODO: auto rang
        self.phone_label.move(20, 180)
        self.phone_entry = QLineEdit(self, placeholderText='phone')
        self.phone_entry.move(150, 180)

        self.delete_button = QPushButton('Удалить читателя', self)

        self.delete_button.setGeometry(380, 108, 150, 30)
        self.delete_button.setStyleSheet('background: rgb(255,0,0);')
        self.delete_button.setStyleSheet("""
        QPushButton{
            font-style: oblique;
            font-weight: bold;
            border: 1px solid #1DA1F2;
            border-radius: 15px;
            color: #1DA1F2;
            background-color: #fff;
        }
        """)
        self.delete_entry = QLineEdit(self, placeholderText='id читателя')
        self.delete_entry.move(550, 110)
        self.delete_button.clicked.connect(self.delete_user)

        # -------------------------------------------кнопки------------------------------------------------
        self.add_button = QPushButton('Добавить читателя', self)
        self.add_button.setGeometry(20, 240, 170, 30)
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
        self.add_button.clicked.connect(self.add_reader)

        self.show_button = QPushButton('Показать читателей', self)
        self.show_button.setGeometry(200, 240, 150, 30)
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
        self.show_button.clicked.connect(self.show_readers)

        self.sort_button = QPushButton('Отсортировать по рангу', self)
        self.sort_button.setGeometry(20, 280, 170, 30)
        self.sort_button.setStyleSheet("""
        QPushButton{
            font-style: oblique;
            font-weight: bold;
            border: 1px solid #1DA1F2;
            border-radius: 15px;
            color: #1DA1F2;
            background-color: #fff;
        }
        """)
        self.sort_button.clicked.connect(self.sort_user_rang)

        # создаем текстовый виджет для вывода списка людей
        self.output = QTextEdit(self)
        self.output.setGeometry(20, 320, 360, 250)

    # -----------------------------------------------функции-------------------------------------------------

    def add_reader(self,obj):
        #from pril_main import MainWindow
        # получаем данные из полей ввода
        name = self.name_entry.text()
        rang = self.rang_entry.text()
        phone = self.phone_entry.text()

        #--------------ПРОВЕРКИ----------------
        if any(map(str.isdigit, name)):
            self.output.clear()
            return self.output.append(f'Имя пользоватлея введено не корректно! Оно должно содержать только буквы!')
        if not rang.isnumeric():
            self.output.clear()
            return self.output.append(f'Ранг введен не корректно! Введите целое положительное число!')
        if int(rang) > 3 or int(rang) < 1:
            self.output.clear()
            return self.output.append('Ранг должен быть целым числом от 1 до 3')
        if not phone.isnumeric():
            self.output.clear()
            return self.output.append(f'Телефон пользоватлея введен не корректно! Номер телефона должен содержать только числа!')
        if len(phone)!=11:
            self.output.clear()
            return self.output.append('Такого номера не существует')
        if name == '':
            self.output.clear()
            return self.output.append(f'Введите имя читателя!')
        if rang == '':
            self.output.clear()
            return self.output.append(f'Введите ранг читателя!')
        if phone == '':
            self.output.clear()
            return self.output.append(f'Введите телефон читателя!')

        # добавляем читателя в базу данных
        self.cur.execute('INSERT OR REPLACE INTO users (name, rang, phone) VALUES (?, ?, ?)',
                         (name, rang, phone))
        self.conn.commit()

        self.conn.commit()

        main_window.init_users_qb()

        # очищаем поля ввода!!!
        self.name_entry.setText('')
        self.rang_entry.setText('')
        self.phone_entry.setText('')

        self.output.clear()

        self.output.append(f'Пользователь {name} успешно добавлен!')

    # функция для вывода списка читателей из базы данных
    def show_readers(self):
        # получаем всех читателей из базы данных
        self.cur.execute('SELECT * FROM users ORDER BY name ASC')
        readers = self.cur.fetchall()
        # очищаем текстовый виджет
        self.output.clear()
        # выводим список книг в текстовый виджет
        i = 1
        for r in readers:
            self.output.append(f'{i}) id - {r[0]}.  {r[1]}, ранг {r[2]}, {r[3]};')
            i += 1

    #удалить пользователя
    def delete_user(self,obj):
        user_id = self.delete_entry.text()
        if not user_id.isnumeric():
            self.output.clear()
            return self.output.append(f'ID пользователя введено не корректно! Введите целое число!')

        flag = False
        for cur_user_id in self.cur.execute('SELECT user_id FROM users').fetchall():
            if str(cur_user_id[0]) == user_id:#str бл!!!!!
                flag = True
        if not flag:
            self.output.clear()
            return self.output.append(f"Пользователя с id - {user_id} не сущетсвует!")
        else:
            name_user = self.cur.execute('SELECT name FROM users WHERE user_id = ?', (user_id,)).fetchall()[0][0]
            self.cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            self.conn.commit()
            self.delete_entry.setText('')
            self.output.clear()
            self.output.append(f"Пользователь {name_user} успешно удален!")
        main_window.init_users_qb()
    def sort_user_rang(self):
        sort_user = self.cur.execute("SELECT * FROM users ORDER BY rang DESC")
        self.output.clear()
        for cur_sort_user in sort_user:
            self.output.append(f"{cur_sort_user[0]}. {cur_sort_user[1]}, ранг {cur_sort_user[2]}, {cur_sort_user[3]};")


    def closeEvent(self, event):
        # закрываем соединение с базой данных при закрытии приложения
        self.conn.close()


if __name__ == '__main__':
    app = QApplication(
        sys.argv)  # создаем экзэмпляр класса. аргументы sys.argv используются для инициализации QApplication

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())  # sys.exit() гарантирует, что приложение завершится
    # корректно при завершении цикла обработки событий(app.exec_()).
