import sqlite3

# создание базы данных и таблицы
conn = sqlite3.connect('library.db')
cur = conn.cursor()

# cur.execute('''CREATE TABLE IF NOT EXISTS issues
#              (id INTEGER PRIMARY KEY AUTOINCREMENT,
#               b_id INTEGER,
#               u_id INTEGER,
#               FOREIGN KEY(b_id) REFERENCES books(book_id),
#               FOREIGN KEY(u_id) REFERENCES readers(user_id))''')
# cur.execute("DROP TABLE issues")
conn.commit()
#Это выражение создает ограничение внешнего ключа на столбец
# "b_id" в текущей таблице, ссылающееся на столбец "book_id" в
# таблице "books". Это гарантирует, что любое значение, введенное в
# столбец "b_id" текущей таблицы, должно существовать в качестве значения
# первичного ключа в столбце "book_id" таблицы "books". Это поддерживает ссылочную
# целостность между двумя таблицами и предотвращает несоответствия данных