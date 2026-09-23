import sqlite3
from datetime import date

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
        valor REAL NOT NULL check (valor > 0),
        categoria_id INTEGER NOT NULL,
        dia_vencimento integer NOT NULL check (dia_vencimento BETWEEN 1 AND 31),
        ativo INTEGER NOT NULL DEFAULT 1 check (ativo IN (0, 1)),
        FOREIGN KEY (categoria_id) REFERENCES categorias (id)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS despesas_fixas_ocorrencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        despesa_fixa_id INTEGER NOT NULL,
        competencia TEXT NOT NULL,
        valor REAL NOT NULL check (valor > 0),
        data_pagamento TEXT,
        status TEXT NOT NULL check (status IN ('pendente', 'pago')),
        check ((data_pagamento IS NOT NULL AND status = 'pago') OR (data_pagamento IS NULL AND status = 'pendente')),
        UNIQUE (despesa_fixa_id, competencia),
        FOREIGN KEY (despesa_fixa_id) REFERENCES despesas_fixas (id)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS despesas_variaveis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL check (valor > 0),
        categoria_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        FOREIGN KEY (categoria_id) REFERENCES categorias (id)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS receitas_fixas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL check (valor > 0)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS receitas_fixas_ocorrencias(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        receita_fixa_id INTEGER NOT NULL,
        competencia TEXT NOT NULL,
        valor REAL NOT NULL check(valor > 0),
        data_recebimento TEXT,
        status TEXT NOT NULL check (status IN ('prevista', 'recebida')),
        UNIQUE (receita_fixa_id, competencia),
        FOREIGN KEY (receita_fixa_id) references receitas_fixas (id)
                )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS receitas_variaveis (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL check (valor > 0),
        data TEXT NOT NULL
                   )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS metas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        descricao TEXT NOT NULL,
        valor_objetivo REAL NOT NULL check (valor_objetivo > 0),
        valor_mensal REAL NOT NULL check (valor_mensal > 0),
        data_criacao TEXT NOT NULL,
        data_conclusao TEXT
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS aportes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meta_id INTEGER NOT NULL,
        valor REAL NOT NULL check (valor > 0),
        data TEXT NOT NULL,
        FOREIGN KEY (meta_id) REFERENCES metas (id)
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS resgates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        meta_id INTEGER NOT NULL,
        valor REAL NOT NULL check (valor > 0),
        data TEXT NOT NULL,
        FOREIGN KEY (meta_id) REFERENCES metas (id)
    )''')

    connect.commit()
    connect.close()
    
def conectar():
    connect = sqlite3.connect('database.db')
    connect.row_factory = sqlite3.Row
    pragma = "PRAGMA foreign_keys = ON"
    cursor = connect.cursor()
    cursor.execute(pragma)
    return connect
        
def buscar_categorias():
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
                          despesas_fixas.dia_vencimento,
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

def buscar_metas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""SELECT metas.id,
                          metas.nome,
                          metas.descricao,
                          metas.valor_objetivo,
                          metas.valor_mensal,
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
    
def salvar_metas(nome, descricao, valor_objetivo,valor_mensal, data_criacao, data_conclusao=None):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("INSERT INTO metas (nome, descricao, valor_objetivo,valor_mensal, data_criacao, data_conclusao) VALUES (?, ?, ?, ?, ?, ?)",
                   (nome, descricao, valor_objetivo, valor_mensal, data_criacao, data_conclusao))
    conexao.commit()
    conexao.close()

def buscar_aportes_por_meta(meta_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM aportes WHERE meta_id = ?", (meta_id,))
    aportes = cursor.fetchall()

    conexao.close()

    return aportes

def buscar_aportes_por_competencia(meta_id, competencia):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT * FROM aportes WHERE meta_id = ? AND data LIKE ?", (meta_id, competencia + '%'))
    aportes = cursor.fetchall()

    conexao.close()

    return aportes

def buscar_valor_meta(meta_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT valor_mensal FROM metas WHERE id = ?", (meta_id,))
    meta = cursor.fetchone()

    conexao.close()

    return meta['valor_mensal'] if meta else None
    
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
    
def salvar_despesa_fixa(descricao, valor, categoria_id, dia_vencimento):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''INSERT INTO despesas_fixas (descricao, valor, categoria_id, dia_vencimento) values (?,?,?,?) ''',
                   (descricao, valor, categoria_id, dia_vencimento))
    id_atual = cursor.lastrowid
    competencia = date.today().strftime('%Y-%m')
    ocorrencia = salvar_despesa_fixa_ocorrencia(conexao,id_atual,competencia)
    
    conexao.commit()
    conexao.close()
    return ocorrencia
   
def salvar_despesa_fixa_ocorrencia(conexao, despesa_fixa_id, competencia, data_pagamento=None, status='pendente'):
    cursor = conexao.cursor()
    
    cursor.execute("INSERT INTO despesas_fixas_ocorrencias (despesa_fixa_id, competencia, valor, data_pagamento, status) VALUES (?, ?,(SELECT valor FROM despesas_fixas WHERE id = ?), ?, ?)",
                   (despesa_fixa_id, competencia, despesa_fixa_id, data_pagamento, status))

def buscar_despesas_fixas_ocorrencias():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""SELECT despesas_fixas_ocorrencias.id,
                          despesas_fixas_ocorrencias.despesa_fixa_id,
                          categorias.nome AS categoria_nome,
                          despesas_fixas_ocorrencias.competencia,
                          despesas_fixas_ocorrencias.valor,
                          despesas_fixas_ocorrencias.data_pagamento,
                          despesas_fixas_ocorrencias.status,
                          despesas_fixas.descricao AS despesa_fixa_descricao
                   FROM despesas_fixas_ocorrencias
                   INNER JOIN despesas_fixas ON despesas_fixas_ocorrencias.despesa_fixa_id = despesas_fixas.id
                   INNER JOIN categorias ON despesas_fixas.categoria_id = categorias.id;""")
    ocorrencias = cursor.fetchall()

    conexao.close()

    return ocorrencias

def pagar_despesa_fixa_ocorrencia(ocorrencia_id, data_pagamento):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("SELECT despesas_fixas_ocorrencias.status, despesas_fixas_ocorrencias.id, despesas_fixas_ocorrencias.despesa_fixa_id, despesas_fixas_ocorrencias.competencia FROM despesas_fixas_ocorrencias WHERE id = ?", (ocorrencia_id,))
    ocorrencia = cursor.fetchone()  # Verifica se a ocorrência existe

    try:
        
        if ocorrencia is None:
            raise ValueError(f"Ocorrência com ID {ocorrencia_id} não encontrada.")
    
        if ocorrencia[0] == 'pago':
            raise ValueError(f"Ocorrência com ID {ocorrencia_id} já está paga.")

        cursor.execute("UPDATE despesas_fixas_ocorrencias SET data_pagamento = ?, status = 'pago' WHERE id = ?",
                       (data_pagamento, ocorrencia_id))
        criar_proxima_ocorrencia(conexao, ocorrencia[2], ocorrencia[3])  # Cria a próxima ocorrência depois de atualizar a atual
        conexao.commit()
    finally:
        conexao.close()
        
def criar_proxima_ocorrencia(conexao,despesa_fixa_id, competencia):
    cursor = conexao.cursor()
    
    cursor.execute("SELECT ativo FROM despesas_fixas WHERE id = ?", (despesa_fixa_id,))
    despesa_ativa = cursor.fetchone()
    
    if despesa_ativa is None or despesa_ativa[0] == 0:
        return 'Despesa Inativa' # Não cria a próxima ocorrência se a despesa fixa não estiver ativa
    
    ano, mes = competencia.split('-')
    mes = int(mes)
    ano = int(ano)
    
    mes += 1
    if mes > 12:
        mes = 1
        ano += 1
    nova_competencia = f"{ano}-{mes:02d}"
    
    # Insere a nova ocorrência
    cursor.execute("INSERT INTO despesas_fixas_ocorrencias (despesa_fixa_id, competencia, valor, status) VALUES (?, ?, (SELECT valor FROM despesas_fixas WHERE id = ?), 'pendente')",
                   (despesa_fixa_id, nova_competencia, despesa_fixa_id))
    
def buscar_despesas_fixas_ocorrencias_por_competencia(competencia):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""SELECT despesas_fixas_ocorrencias.id,
                          despesas_fixas_ocorrencias.despesa_fixa_id,
                          categorias.nome AS categoria_nome,
                          despesas_fixas_ocorrencias.competencia,
                          despesas_fixas_ocorrencias.valor,
                          despesas_fixas_ocorrencias.data_pagamento,
                          despesas_fixas_ocorrencias.status,
                          despesas_fixas.descricao AS despesa_fixa_descricao
                   FROM despesas_fixas_ocorrencias
                   INNER JOIN despesas_fixas ON despesas_fixas_ocorrencias.despesa_fixa_id = despesas_fixas.id
                   INNER JOIN categorias ON despesas_fixas.categoria_id = categorias.id
                   WHERE despesas_fixas_ocorrencias.competencia = ?;""", (competencia,))
    ocorrencias = cursor.fetchall()

    conexao.close()

    return ocorrencias

def buscar_despesas_variaveis_por_competencia(competencia):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''SELECT despesas_variaveis.id,
                    categorias.nome as categoria_nome,
                    despesas_variaveis.descricao,
                    despesas_variaveis.valor,
                    despesas_variaveis.data
                FROM despesas_variaveis
                INNER JOIN categorias ON despesas_variaveis.categoria_id = categorias.id
                WHERE despesas_variaveis.data LIKE ?''', (competencia + '%',))
    contas_variaveis = cursor.fetchall()
    conexao.close()
    return contas_variaveis

def salvar_receita_fixa(nome, descricao, valor):
    conexao = conectar()
    cursor = conexao.cursor()
        
    cursor.execute('''INSERT INTO receitas_fixas (nome, descricao, valor) VALUES (?,?,?)''',
                    (nome, descricao, valor))
    id_criado = cursor.lastrowid
       
    salvar_receita_fixa_ocorrencias(conexao, id_criado)
    
    conexao.commit()
    cursor.close()
    conexao.close()
    
def buscar_receitas_fixas():
    conexao = conectar()
    cursor = conexao.cursor()
        
    cursor.execute('''SELECT *
                       FROM receitas_fixas''')
    
    receitas_fixas = cursor.fetchall()
    conexao.close()
    
    return receitas_fixas

def salvar_receita_fixa_ocorrencias(conexao, receita_fixa_id, data_recebimento = None, status = 'prevista'):
    cursor = conexao.cursor()
        
    competencia = date.today().strftime('%Y-%m')
    cursor.execute("INSERT INTO receitas_fixas_ocorrencias (receita_fixa_id, competencia, valor, data_recebimento, status) VALUES (?, ?,(SELECT valor FROM receitas_fixas WHERE id = ?), ?, ?)",
                       (receita_fixa_id, competencia, receita_fixa_id, data_recebimento, status))

def buscar_receitas_fixas_ocorrencias_por_competencia(competencia):
    conexao = conectar()
    cursor = conexao.cursor()
            
    cursor.execute('''SELECT receitas_fixas_ocorrencias.id,
                   receitas_fixas.id,
                   receitas_fixas.nome,
                   receitas_fixas_ocorrencias.competencia,
                   receitas_fixas_ocorrencias.valor,
                   receitas_fixas_ocorrencias.data_recebimento,
                   receitas_fixas_ocorrencias.status
                   FROM receitas_fixas_ocorrencias
                   INNER JOIN receitas_fixas ON receitas_fixas_ocorrencias.receita_fixa_id = receitas_fixas.id
                   WHERE receitas_fixas_ocorrencias.competencia = ?
                   ''', (competencia,))
    ocorrencias = cursor.fetchall()
    
    conexao.close()
    
    return ocorrencias

def receber_receita_fixa_ocorrencia(data_recebimento, ocorrencia_id):
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('''SELECT receitas_fixas_ocorrencias.id,
                   receitas_fixas_ocorrencias.receita_fixa_id,
                   receitas_fixas_ocorrencias.competencia,
                   receitas_fixas_ocorrencias.data_recebimento,
                   receitas_fixas_ocorrencias.status
                   FROM receitas_fixas_ocorrencias
                   WHERE id = ?''', (ocorrencia_id,))
    ocorrencia = cursor.fetchone()
    
    try:
        
        if ocorrencia == None:
            raise ValueError(f"Ocorrência com ID {ocorrencia_id} não encontrada.")
        
        if ocorrencia[4] == 'recebida':
            raise ValueError(f"Ocorrência com ID {ocorrencia_id} já foi recebida.")
        
        cursor.execute('''UPDATE receitas_fixas_ocorrencias SET data_recebimento = ?, status = 'recebida' WHERE id = ? ''',
                       (data_recebimento, ocorrencia_id))
        criar_proxima_ocorrencia_receitas(conexao, ocorrencia[1], ocorrencia[2])
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()
        
def criar_proxima_ocorrencia_receitas(conexao, receita_fixa_id, competencia):
    cursor = conexao.cursor()
        
    ano, mes = competencia.split('-')
    mes = int(mes)
    ano = int(ano)
        
    mes += 1
    if mes > 12:
            mes = 1
            ano += 1
    nova_competencia = f"{ano}-{mes:02d}"
        
        # Insere a nova ocorrência
    cursor.execute("INSERT INTO receitas_fixas_ocorrencias (receita_fixa_id, competencia, valor, status) VALUES (?, ?, (SELECT valor FROM receitas_fixas WHERE id = ?), 'prevista')",
                       (receita_fixa_id, nova_competencia, receita_fixa_id))
    
def salvar_receita_variavel(nome, descricao, valor, data):
    conexao = conectar()
    cursor = conexao.cursor()
        
    cursor.execute('''INSERT INTO receitas_variaveis (nome, descricao, valor, data) VALUES (?,?,?,?) ''',
                   (nome, descricao, valor, data))
    
    conexao.commit()
    conexao.close()
    
def buscar_receitas_variaveis_por_competencia(competencia):
    conexao = conectar()
    cursor = conexao.cursor()
            
    cursor.execute('''SELECT *
                   FROM receitas_variaveis
                   WHERE data LIKE ?''',
                   (competencia + '%',))
    receitas_variaveis_por_competencia = cursor.fetchall()
    conexao.close()
    return receitas_variaveis_por_competencia