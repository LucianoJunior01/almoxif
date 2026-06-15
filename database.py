import sqlite3

def conectar():
    conn = sqlite3.connect('almoxarifado.db')
    conn.row_factory = sqlite3.Row
    return conn

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS fornecedor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cnpj TEXT,
            telefone TEXT,
            email TEXT
        );

        CREATE TABLE IF NOT EXISTS produto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            codigo TEXT UNIQUE NOT NULL,
            categoria TEXT,
            unidade TEXT,
            estoque_atual REAL DEFAULT 0,
            estoque_minimo REAL DEFAULT 0,
            preco_medio REAL DEFAULT 0,
            nacional TEXT DEFAULT 'S',
            pais_origem TEXT,
            lead_time_dias INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS movimentacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL,
            produto_id INTEGER NOT NULL,
            fornecedor_id INTEGER,
            quantidade REAL NOT NULL,
            preco_unitario REAL,
            numero_nf TEXT,
            data TEXT NOT NULL,
            motivo TEXT,
            responsavel TEXT,
            FOREIGN KEY (produto_id) REFERENCES produto(id),
            FOREIGN KEY (fornecedor_id) REFERENCES fornecedor(id)
        );
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    criar_tabelas()
    print("Banco de dados criado com sucesso!")