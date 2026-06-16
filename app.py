from flask import Flask, render_template
from database import criar_tabelas, conectar
from routes.produtos import produtos_bp
from routes.fornecedores import fornecedores_bp
from routes.movimentacoes import movimentacoes_bp
from routes.relatorios import relatorios_bp
import psycopg2.extras
from datetime import date

app = Flask(__name__)
app.register_blueprint(produtos_bp)
app.register_blueprint(fornecedores_bp)
app.register_blueprint(movimentacoes_bp)
app.register_blueprint(relatorios_bp)
criar_tabelas()

@app.route('/')
def dashboard():
    conn = conectar()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor.execute('SELECT COUNT(*) as total FROM produto')
    total_produtos = cursor.fetchone()['total']

    cursor.execute('SELECT COUNT(*) as total FROM produto WHERE estoque_atual < estoque_minimo')
    estoque_baixo = cursor.fetchone()['total']

    hoje = date.today().isoformat()

    cursor.execute('SELECT COUNT(*) as total FROM movimentacao WHERE tipo=%s AND data=%s', ('E', hoje))
    entradas_hoje = cursor.fetchone()['total']

    cursor.execute('SELECT COUNT(*) as total FROM movimentacao WHERE tipo=%s AND data=%s', ('S', hoje))
    saidas_hoje = cursor.fetchone()['total']

    cursor.close()
    conn.close()

    return render_template('dashboard.html',
        total_produtos=total_produtos,
        estoque_baixo=estoque_baixo,
        entradas_hoje=entradas_hoje,
        saidas_hoje=saidas_hoje
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)