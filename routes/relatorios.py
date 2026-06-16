from flask import Blueprint, render_template, request
from database import conectar
import psycopg2.extras

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/relatorios')
def index():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute('''
        SELECT nome, codigo, categoria, unidade,
               estoque_atual, estoque_minimo, preco_medio,
               (estoque_atual * preco_medio) as valor_total,
               nacional, pais_origem, lead_time_dias
        FROM produto ORDER BY nome
    ''')
    produtos = cursor.fetchall()

    cursor.execute('''
        SELECT nome, codigo, estoque_atual, estoque_minimo, unidade
        FROM produto WHERE estoque_atual < estoque_minimo ORDER BY nome
    ''')
    estoque_baixo = cursor.fetchall()

    data_inicio = request.args.get('data_inicio', '')
    data_fim = request.args.get('data_fim', '')

    if data_inicio and data_fim:
        cursor.execute('''
            SELECT m.*, p.nome as produto_nome, f.nome as fornecedor_nome
            FROM movimentacao m
            JOIN produto p ON m.produto_id = p.id
            LEFT JOIN fornecedor f ON m.fornecedor_id = f.id
            WHERE m.data BETWEEN %s AND %s
            ORDER BY m.data DESC
        ''', (data_inicio, data_fim))
    else:
        cursor.execute('''
            SELECT m.*, p.nome as produto_nome, f.nome as fornecedor_nome
            FROM movimentacao m
            JOIN produto p ON m.produto_id = p.id
            LEFT JOIN fornecedor f ON m.fornecedor_id = f.id
            ORDER BY m.id DESC LIMIT 20
        ''')
    movimentacoes = cursor.fetchall()

    cursor.execute('SELECT COUNT(*) as total FROM produto')
    total_produtos = cursor.fetchone()['total']

    cursor.execute('SELECT COALESCE(SUM(quantidade), 0) as total FROM movimentacao WHERE tipo=%s', ('E',))
    total_entradas = cursor.fetchone()['total']

    cursor.execute('SELECT COALESCE(SUM(quantidade), 0) as total FROM movimentacao WHERE tipo=%s', ('S',))
    total_saidas = cursor.fetchone()['total']

    valor_total_estoque = sum(p['valor_total'] for p in produtos)

    cursor.close()
    conn.close()

    return render_template('relatorios/index.html',
        produtos=produtos,
        estoque_baixo=estoque_baixo,
        movimentacoes=movimentacoes,
        total_produtos=total_produtos,
        valor_total_estoque=valor_total_estoque,
        total_entradas=total_entradas,
        total_saidas=total_saidas,
        data_inicio=data_inicio,
        data_fim=data_fim
    )