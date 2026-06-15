from flask import Blueprint, render_template, request, redirect, url_for
from database import conectar
from datetime import date

movimentacoes_bp = Blueprint('movimentacoes', __name__)

@movimentacoes_bp.route('/movimentacoes')
def listar():
    conn = conectar()
    movimentacoes = conn.execute('''
        SELECT m.*, p.nome as produto_nome, f.nome as fornecedor_nome
        FROM movimentacao m
        JOIN produto p ON m.produto_id = p.id
        LEFT JOIN fornecedor f ON m.fornecedor_id = f.id
        ORDER BY m.id DESC
    ''').fetchall()
    conn.close()
    return render_template('movimentacoes/listar.html', movimentacoes=movimentacoes)

@movimentacoes_bp.route('/movimentacoes/entrada', methods=['GET', 'POST'])
def entrada():
    conn = conectar()
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        quantidade = float(request.form['quantidade'])
        preco_unitario = float(request.form['preco_unitario'])

        # Registra a movimentação
        conn.execute('''
            INSERT INTO movimentacao 
            (tipo, produto_id, fornecedor_id, quantidade, preco_unitario, numero_nf, data, motivo, responsavel)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            'E',
            produto_id,
            request.form['fornecedor_id'],
            quantidade,
            preco_unitario,
            request.form['numero_nf'],
            request.form['data'],
            request.form['motivo'],
            request.form['responsavel']
        ))

        # Atualiza o estoque do produto
        conn.execute('''
            UPDATE produto 
            SET estoque_atual = estoque_atual + ?,
                preco_medio = ?
            WHERE id = ?
        ''', (quantidade, preco_unitario, produto_id))

        conn.commit()
        conn.close()
        return redirect(url_for('movimentacoes.listar'))

    produtos = conn.execute('SELECT * FROM produto ORDER BY nome').fetchall()
    fornecedores = conn.execute('SELECT * FROM fornecedor ORDER BY nome').fetchall()
    conn.close()
    return render_template('movimentacoes/entrada.html',
        produtos=produtos,
        fornecedores=fornecedores,
        hoje=date.today().isoformat()
    )

@movimentacoes_bp.route('/movimentacoes/saida', methods=['GET', 'POST'])
def saida():
    conn = conectar()
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        quantidade = float(request.form['quantidade'])

        # Registra a movimentação
        conn.execute('''
            INSERT INTO movimentacao 
            (tipo, produto_id, quantidade, data, motivo, responsavel)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            'S',
            produto_id,
            quantidade,
            request.form['data'],
            request.form['motivo'],
            request.form['responsavel']
        ))

        # Atualiza o estoque do produto
        conn.execute('''
            UPDATE produto 
            SET estoque_atual = estoque_atual - ?
            WHERE id = ?
        ''', (quantidade, produto_id))

        conn.commit()
        conn.close()
        return redirect(url_for('movimentacoes.listar'))

    produtos = conn.execute('SELECT * FROM produto ORDER BY nome').fetchall()
    conn.close()
    return render_template('movimentacoes/saida.html',
        produtos=produtos,
        hoje=date.today().isoformat()
    )