from flask import Flask, render_template
from database import criar_tabelas, conectar
from routes.produtos import produtos_bp
from routes.fornecedores import fornecedores_bp
from routes.movimentacoes import movimentacoes_bp
from routes.relatorios import relatorios_bp

app = Flask(__name__)
app.register_blueprint(produtos_bp)
app.register_blueprint(fornecedores_bp)
app.register_blueprint(movimentacoes_bp)
app.register_blueprint(relatorios_bp)
criar_tabelas()

@app.route('/')
def dashboard():
    conn = conectar()
    cursor = conn.cursor()

    total_produtos = cursor.execute('SELECT COUNT(*) FROM produto').fetchone()[0]
    estoque_baixo = cursor.execute(
        'SELECT COUNT(*) FROM produto WHERE estoque_atual < estoque_minimo'
    ).fetchone()[0]

    hoje = __import__('datetime').date.today().isoformat()
    entradas_hoje = cursor.execute(
        'SELECT COUNT(*) FROM movimentacao WHERE tipo="E" AND data=?', (hoje,)
    ).fetchone()[0]
    saidas_hoje = cursor.execute(
        'SELECT COUNT(*) FROM movimentacao WHERE tipo="S" AND data=?', (hoje,)
    ).fetchone()[0]

    conn.close()
    return render_template('dashboard.html',
        total_produtos=total_produtos,
        estoque_baixo=estoque_baixo,
        entradas_hoje=entradas_hoje,
        saidas_hoje=saidas_hoje
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)