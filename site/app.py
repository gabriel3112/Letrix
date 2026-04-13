from flask import Flask, render_template, jsonify
import mysql.connector
import random

app = Flask(__name__)

# ==========================================
# Configuração do Banco de Dados
# ==========================================
# Substitua 'sua_senha' pela senha do seu MySQL, se houver.
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '', 
    'database': 'LETRIX'
}

def conectar_banco():
    """Cria e retorna uma conexão com o banco de dados."""
    return mysql.connector.connect(**db_config)

# ==========================================
# Rotas (Caminhos do seu site)
# ==========================================

@app.route('/')
def introducao():
    """Rota para a página inicial."""
    return render_template('intro.html')

@app.route('/jogo')
def jogo():
    """Rota para a página principal do jogo."""
    return render_template('main.html')

@app.route('/letrix')
def letrix_api():
    """API que fornece uma palavra aleatória do banco de dados para o JavaScript."""
    try:
        conexao = conectar_banco()
        cursor = conexao.cursor(dictionary=True)
        
        # Busca todas as palavras e imagens cadastradas na tabela 'palavras'
        cursor.execute("SELECT palavra, imagem FROM palavras")
        resultados = cursor.fetchall()
        
        cursor.close()
        conexao.close()

        if resultados:
            # Sorteia uma palavra da lista para enviar ao jogo
            palavra_sorteada = random.choice(resultados)
            return jsonify(palavra_sorteada)
        else:
            return jsonify({"erro": "Nenhuma palavra encontrada no banco de dados."}), 404

    except mysql.connector.Error as erro_bd:
        print(f"Erro de Banco de Dados: {erro_bd}")
        return jsonify({"erro": "Erro ao conectar com o banco de dados."}), 500
    except Exception as e:
        print(f"Erro geral: {e}")
        return jsonify({"erro": "Erro interno do servidor."}), 500

# ==========================================
# Executar o Servidor
# ==========================================
if __name__ == '__main__':
    # O debug=True faz com que o servidor reinicie sozinho se você alterar o código
    app.run(debug=True, port=5000)