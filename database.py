import sqlite3

def create_database():
    connect = sqlite3.connect('database.db')
    pragma = "PRAGMA foreign_keys = ON"
    cursor = connect.cursor()
    cursor.execute(pragma)

    cursor.execute('''CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS despesas_fixas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        categoria_id INTEGER NOT NULL,
        data_vencimento TEXT NOT NULL,
        active TEXT NOT NULL DEFAULT 'yes',
        FOREIGN KEY (categoria_id) REFERENCES categorias (id)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS despesas_variaveis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        categoria_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorias (id)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS receitas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        data TEXT NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS metas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL,
        valor_objetivo REAL NOT NULL,
        data_criacao TEXT,
        data_conclusao TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS aportes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meta_id INTEGER NOT NULL,
        valor REAL NOT NULL,
        data TEXT NOT NULL,
        FOREIGN KEY (meta_id) REFERENCES metas (id)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS resgates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meta_id INTEGER NOT NULL,
        valor REAL NOT NULL,
        data TEXT NOT NULL,
        FOREIGN KEY (meta_id) REFERENCES metas (id)
    )''')
    cursor.execute('''DROP TABLE IF EXISTS gastos''')

    connect.commit()
    connect.close()
    
def conectar():
    connect = sqlite3.connect('database.db')
    pragma = "PRAGMA foreign_keys = ON"
    cursor = connect.cursor()
    cursor.execute(pragma)
    return connect
    
def insert_initial_data():
        connect = sqlite3.connect('database.db')
        pragma = "PRAGMA foreign_keys = ON"
        cursor = connect.cursor()
        cursor.execute(pragma)

        # Inserir categorias iniciais
        categorias = ['Alimentação']
        for categoria in categorias:
            cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (categoria,))
            id_gerado = cursor.lastrowid
        # Inserir despesas fixas iniciais
        despesas_fixas = [
            ('Aluguel', 1500.00, id_gerado, '2024-07-01'),
        ]
        for descricao, valor, categoria_id, data_vencimento in despesas_fixas:
            cursor.execute("INSERT INTO despesas_fixas (descricao, valor, categoria_id, data_vencimento) VALUES (?, ?, ?, ?)",
                           (descricao, valor, categoria_id, data_vencimento))

        # Inserir despesas variáveis iniciais
        despesas_variaveis = [
            ('Supermercado', 400.00, id_gerado, '2024-07-02'),
        ]
        for descricao, valor, categoria_id, data in despesas_variaveis:
            cursor.execute("INSERT INTO despesas_variaveis (descricao, valor, categoria_id, data) VALUES (?, ?, ?, ?)",
                           (descricao, valor, categoria_id, data))

        # Inserir receitas iniciais
        receitas = [
            ('Salário', 'Salário mensal', 5000.00, '2024-07-01'),
            ('Freelance', 'Projeto freelance', 800.00, '2024-07-15')
        ]
        for nome, descricao, valor, data in receitas:
            cursor.execute("INSERT INTO receitas (nome, descricao, valor, data) VALUES (?, ?, ?, ?)",
                           (nome, descricao, valor, data))

        # Inserir metas iniciais
        metas = [
            ('Viagem para a Europa', 'Economizar para viagem de férias', 10000.00),
        ]
        for nome, descricao, valor_objetivo in metas:
            cursor.execute("INSERT INTO metas (nome, descricao, valor_objetivo) VALUES (?, ?, ?)",
                           (nome, descricao, valor_objetivo))
            id_gerado_meta = cursor.lastrowid
        aportes = [
            (id_gerado_meta, 2000.00, '2024-07-10'),
        ]
        for meta_id, valor, data in aportes:
            cursor.execute("INSERT INTO aportes (meta_id, valor, data) VALUES (?, ?, ?)",
                           (meta_id, valor, data))
        connect.commit()
        connect.close()
        
def bucar_categorias():
    conexao = conectar()

    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()

    conexao.close()

    return categorias

def buscar_despesas_fixas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""SELECT despesas_fixas.id,
                          despesas_fixas.descricao,
                          despesas_fixas.valor,
                          despesas_fixas.data_vencimento,
                          categorias.nome AS categoria_nome 
                   FROM despesas_fixas
                   INNER JOIN categorias ON despesas_fixas.categoria_id = categorias.id;""")
    despesas_fixas = cursor.fetchall()

    conexao.close()

    return despesas_fixas

def buscar_despesas_variaveis():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""SELECT despesas_variaveis.id,
                          despesas_variaveis.descricao,
                          despesas_variaveis.valor,
                          despesas_variaveis.data,
                          categorias.nome AS categoria_nome 
                   FROM despesas_variaveis
                   INNER JOIN categorias ON despesas_variaveis.categoria_id = categorias.id;""")
    despesas_variaveis = cursor.fetchall()

    conexao.close()

    return despesas_variaveis

def buscar_receitas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""SELECT receitas.id,
                          receitas.nome,
                          receitas.descricao,
                          receitas.valor,
                          receitas.data
                   FROM receitas""")
    receitas = cursor.fetchall()

    conexao.close()

    return receitas

def buscar_metas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""SELECT metas.id,
                          metas.nome,
                          metas.descricao,
                          metas.valor_objetivo,
                          metas.data_criacao,
                          metas.data_conclusao
                   FROM metas""")
    metas = cursor.fetchall()

    conexao.close()

    return metas

def buscar_aportes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""SELECT aportes.id,
                          aportes.meta_id,
                          aportes.valor,
                          aportes.data,
                          metas.nome AS meta_nome
                   FROM aportes
                   INNER JOIN metas ON aportes.meta_id = metas.id;""")
    aportes = cursor.fetchall()

    conexao.close()

    return aportes

def buscar_resgates():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""SELECT resgates.id,
                          resgates.meta_id,
                          resgates.valor,
                          resgates.data,
                          metas.nome AS meta_nome
                   FROM resgates
                   INNER JOIN metas ON resgates.meta_id = metas.id;""")
    resgates = cursor.fetchall()

    conexao.close()

    return resgates

def salvar_categoria(nome):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
    conexao.commit()
    conexao.close()
    
def salvar_despesa_variavel(descricao, valor, categoria_id, data):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO despesas_variaveis (descricao, valor, categoria_id, data) VALUES (?, ?, ?, ?)",
                   (descricao, valor, categoria_id, data))
    conexao.commit()
    conexao.close()
    
def salvar_despesa_fixa(descricao, valor, categoria_id, data_vencimento):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO despesas_fixas (descricao, valor, categoria_id, data_vencimento) VALUES (?, ?, ?, ?)",
                   (descricao, valor, categoria_id, data_vencimento))
    conexao.commit()
    conexao.close()
    
def salvar_receita(nome, descricao, valor, data):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO receitas (nome, descricao, valor, data) VALUES (?, ?, ?, ?)",
                   (nome, descricao, valor, data))
    conexao.commit()
    conexao.close()
    
def salvar_metas(nome, descricao, valor_objetivo, data_criacao, data_conclusao=None):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO metas (nome, descricao, valor_objetivo, data_criacao, data_conclusao) VALUES (?, ?, ?, ?, ?)",
                   (nome, descricao, valor_objetivo, data_criacao, data_conclusao))
    conexao.commit()
    conexao.close()
    
def salvar_aportes(meta_id, valor, data):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO aportes (meta_id, valor, data) VALUES (?, ?, ?)",
                   (meta_id, valor, data))
    conexao.commit()
    conexao.close()
    
def salvar_resgates(meta_id, valor, data):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO resgates (meta_id, valor, data) VALUES (?, ?, ?)",
                   (meta_id, valor, data))
    conexao.commit()
    conexao.close()
