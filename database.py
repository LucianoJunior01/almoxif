import psycopg2
import psycopg2.extras
import os

DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:BCoZxyTplmCsRmCEgmNynTDVojgUXKGR@thomas.proxy.rlwy.net:59210/railway')
def conectar():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fornecedor (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            cnpj TEXT,
            telefone TEXT,
            email TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produto (
            id SERIAL PRIMARY KEY,
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
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimentacao (
            id SERIAL PRIMARY KEY,
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
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    criar_tabelas()
    print("Banco de dados criado com sucesso!")