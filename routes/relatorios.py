from flask import Blueprint, render_template, request
from database import conectar

relatorios_bp = Blueprint('relatorios', __name__)

@relatorios_bp.route('/relatorios')
def index():
    conn = conectar()

    # Posição atual do estoque
    produtos = conn.execute('''
        SELECT nome, codigo, categoria, unidade,
               estoque_atual, estoque_minimo, preco_medio,
               (estoque_atual * preco_medio) as valor_total,
               nacional, pais_origem, lead_time_dias
        FROM produto
        ORDER BY nome
    ''').fetchall()

    # Produtos com estoque baixo
    estoque_baixo = conn.execute('''
        SELECT nome, codigo, estoque_atual, estoque_minimo, unidade
        FROM produto
        WHERE estoque_atual < estoque_minimo
        ORDER BY nome
    ''').fetchall()

    # Movimentações por período
    data_inicio = request.args.get('data_inicio', '')
    data_fim = request.args.get('data_fim', '')

    if data_inicio and data_fim:
        movimentacoes = conn.execute('''
            SELECT m.*, p.nome as produto_nome, f.nome as fornecedor_nome
            FROM movimentacao m
            JOIN produto p ON m.produto_id = p.id
            LEFT JOIN fornecedor f ON m.fornecedor_id = f.id
            WHERE m.data BETWEEN ? AND ?
            ORDER BY m.data DESC
        ''', (data_inicio, data_fim)).fetchall()
    else:
        movimentacoes = conn.execute('''
            SELECT m.*, p.nome as produto_nome, f.nome as fornecedor_nome
            FROM movimentacao m
            JOIN produto p ON m.produto_id = p.id
            LEFT JOIN fornecedor f ON m.fornecedor_id = f.id
            ORDER BY m.data DESC
            LIMIT 20
        ''').fetchall()

    # Totais gerais
    total_produtos = len(produtos)
    valor_total_estoque = sum(p['valor_total'] for p in produtos)
    total_entradas = conn.execute(
        'SELECT COALESCE(SUM(quantidade), 0) FROM movimentacao WHERE tipo="E"'
    ).fetchone()[0]
    total_saidas = conn.execute(
        'SELECT COALESCE(SUM(quantidade), 0) FROM movimentacao WHERE tipo="S"'
    ).fetchone()[0]

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