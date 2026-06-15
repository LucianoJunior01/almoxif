from flask import Blueprint, render_template, request, redirect, url_for
from database import conectar

fornecedores_bp = Blueprint('fornecedores', __name__)

@fornecedores_bp.route('/fornecedores')
def listar():
    conn = conectar()
    fornecedores = conn.execute('SELECT * FROM fornecedor ORDER BY nome').fetchall()
    conn.close()
    return render_template('fornecedores/listar.html', fornecedores=fornecedores)

@fornecedores_bp.route('/fornecedores/novo', methods=['GET', 'POST'])
def novo():
    if request.method == 'POST':
        conn = conectar()
        conn.execute('''
            INSERT INTO fornecedor (nome, cnpj, telefone, email)
            VALUES (?, ?, ?, ?)
        ''', (
            request.form['nome'],
            request.form['cnpj'],
            request.form['telefone'],
            request.form['email']
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('fornecedores.listar'))
    return render_template('fornecedores/novo.html')

@fornecedores_bp.route('/fornecedores/excluir/<int:id>')
def excluir(id):
    conn = conectar()
    conn.execute('DELETE FROM fornecedor WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('fornecedores.listar'))