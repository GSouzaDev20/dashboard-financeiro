import sqlite3

connect = sqlite3.connect('database.db')
cursor = connect.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS gastos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    descricao TEXT NOT NULL,
    valor REAL NOT NULL
)''')

connect.commit()
connect.close()