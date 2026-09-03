import sqlite3

def create_database():
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS gastos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL
    )''')

    connect.commit()
    connect.close()

def buscar_gastos():
    connect = sqlite3.connect('database.db')
    connect.row_factory = sqlite3.Row

    cursor = connect.cursor()
    cursor.execute("SELECT * FROM gastos")

    gastos = cursor.fetchall()
    print(gastos)

    connect.close()
    return gastos
def conectar():
    connect = sqlite3.connect('database.db')
    return connect
def salvar_gasto(descricao, valor):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    cursor.execute("INSERT INTO gastos (descricao, valor) VALUES (?, ?)", (descricao, valor))

    connect.commit()
    connect.close()