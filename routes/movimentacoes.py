from flask import Blueprint, render_template, request, redirect, url_for
from database import conectar
from datetime import date
import psycopg2.extras

movimentacoes_bp = Blueprint('movimentacoes', __name__)

@movimentacoes_bp.route('/movimentacoes')
def listar():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute('''
        SELECT m.*, p.nome as produto_nome, f.nome as fornecedor_nome
        FROM movimentacao m
        JOIN produto p ON m.produto_id = p.id
        LEFT JOIN fornecedor f ON m.fornecedor_id = f.id
        ORDER BY m.id DESC
    ''')
    movimentacoes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('movimentacoes/listar.html', movimentacoes=movimentacoes)

@movimentacoes_bp.route('/movimentacoes/entrada', methods=['GET', 'POST'])
def entrada():
    conn = conectar()
    if request.method == 'POST':
        produto_id = request.form['produto_id']
        quantidade = float(request.form['quantidade'])
        preco_unitario = float(request.form['preco_unitario'])
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO movimentacao 
            (tipo, produto_id, fornecedor_id, quantidade, preco_unitario, numero_nf, data, motivo, responsavel)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
        cursor.execute('''
            UPDATE produto 
            SET estoque_atual = estoque_atual + %s,
                preco_medio = %s
            WHERE id = %s
        ''', (quantidade, preco_unitario, produto_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('movimentacoes.listar'))

    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute('SELECT * FROM produto ORDER BY nome')
    produtos = cursor.fetchall()
    cursor.execute('SELECT * FROM fornecedor ORDER BY nome')
    fornecedores = cursor.fetchall()
    cursor.close()
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
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO movimentacao 
            (tipo, produto_id, quantidade, data, motivo, responsavel)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (
            'S',
            produto_id,
            quantidade,
            request.form['data'],
            request.form['motivo'],
            request.form['responsavel']
        ))
        cursor.execute('''
            UPDATE produto 
            SET estoque_atual = estoque_atual - %s
            WHERE id = %s
        ''', (quantidade, produto_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('movimentacoes.listar'))

    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute('SELECT * FROM produto ORDER BY nome')
    produtos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('movimentacoes/saida.html',
        produtos=produtos,
        hoje=date.today().isoformat()
    )