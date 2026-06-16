from flask import Blueprint, render_template, request, redirect, url_for
from database import conectar
import psycopg2.extras

fornecedores_bp = Blueprint('fornecedores', __name__)

@fornecedores_bp.route('/fornecedores')
def listar():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute('SELECT * FROM fornecedor ORDER BY nome')
    fornecedores = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('fornecedores/listar.html', fornecedores=fornecedores)

@fornecedores_bp.route('/fornecedores/novo', methods=['GET', 'POST'])
def novo():
    if request.method == 'POST':
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO fornecedor (nome, cnpj, telefone, email)
            VALUES (%s, %s, %s, %s)
        ''', (
            request.form['nome'],
            request.form['cnpj'],
            request.form['telefone'],
            request.form['email']
        ))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('fornecedores.listar'))
    return render_template('fornecedores/novo.html')

@fornecedores_bp.route('/fornecedores/excluir/<int:id>')
def excluir(id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM fornecedor WHERE id = %s', (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('fornecedores.listar'))