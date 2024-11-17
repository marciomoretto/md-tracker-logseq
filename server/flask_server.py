#!/usr/bin/python3

from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa o CORS

import subprocess
import os
import sys

app = Flask(__name__)
CORS(app)  # Habilita o CORS para todas as rotas

# Validação do argumento para o diretório do Vault
if len(sys.argv) != 2:
    print("Uso: python3 server.py /caminho/para/vault")
    sys.exit(1)

# Diretório do Vault
vault_dir = os.path.abspath(sys.argv[1])  # Obtém o caminho absoluto

if not os.path.isdir(vault_dir):
    print(f"Erro: O diretório '{vault_dir}' não é válido.")
    sys.exit(1)

@app.route("/run-script", methods=["GET"])
def run_script():
    # Obtém o parâmetro "pagename" da requisição HTTP GET
    pagename = request.args.get("pagename")
    if not pagename:
        return jsonify({"error": "Nenhuma página fornecida."}), 400
    
    # Gera o caminho completo do arquivo da página no Vault
    file_path = os.path.join(vault_dir, "pages", f"{pagename}.md")

    if not os.path.isfile(file_path):
        return jsonify({"error": f"A página '{pagename}' não foi encontrada no Vault."}), 404
    
    # Caminho do script Python
    script_path = os.path.join(os.path.dirname(__file__), "link_search.py")
    
    try:
        result = subprocess.run(
            ["python3", script_path, file_path],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        
        # Retorna a saída e erros do script como resposta JSON
        return jsonify({
            "output": result.stdout,
            "error": result.stderr
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
