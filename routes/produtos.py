from flask import Blueprint, render_template, request, redirect, url_for
from database import conectar

produtos_bp = Blueprint('produtos', __name__)

@produtos_bp.route('/produtos')
def listar():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=__import__('psycopg2').extras.RealDictCursor)
    cursor.execute('SELECT * FROM produto ORDER BY nome')
    produtos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('produtos/listar.html', produtos=produtos)

@produtos_bp.route('/produtos/novo', methods=['GET', 'POST'])
def novo():
    if request.method == 'POST':
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO produto 
            (nome, codigo, categoria, unidade, estoque_atual, estoque_minimo, preco_medio, nacional, pais_origem, lead_time_dias)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            request.form['nome'],
            request.form['codigo'],
            request.form['categoria'],
            request.form['unidade'],
            request.form['estoque_atual'],
            request.form['estoque_minimo'],
            request.form['preco_medio'],
            request.form['nacional'],
            request.form['pais_origem'],
            request.form['lead_time_dias']
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('produtos.listar'))
    return render_template('produtos/novo.html')

@produtos_bp.route('/produtos/excluir/<int:id>')
def excluir(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM produto WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('produtos.listar'))