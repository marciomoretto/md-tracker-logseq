#!/usr/bin/python3

from flask import Flask, request, jsonify
from flask_cors import CORS  # Importa o CORS

import subprocess
import os
import sys

app = Flask(__name__)
CORS(app)  # Habilita o CORS para todas as rotas

# Validação do argumento para os diretórios monitorados
if len(sys.argv) != 3:
    print("Uso: python3 server.py /caminho/para/pages /caminho/para/journals")
    sys.exit(1)

# Diretórios monitorados
pages_dir = os.path.abspath(sys.argv[1])  # Diretório para "pages"
journals_dir = os.path.abspath(sys.argv[2])  # Diretório para "journals"

if not os.path.isdir(pages_dir):
    print(f"Erro: O diretório 'pages' '{pages_dir}' não é válido.")
    sys.exit(1)

if not os.path.isdir(journals_dir):
    print(f"Erro: O diretório 'journals' '{journals_dir}' não é válido.")
    sys.exit(1)

@app.route("/run-script", methods=["GET"])
def run_script():
    # Obtém os parâmetros "type" e "name" da requisição HTTP GET
    file_type = request.args.get("type")  # Pode ser "page" ou "journal"
    name = request.args.get("name")  # Nome do arquivo sem extensão

    print(name)

    if not file_type or not name:
        return jsonify({"error": "Parâmetros 'type' e 'name' são obrigatórios."}), 400

    # Determina o diretório com base no tipo
    if file_type == "page":
        file_path = os.path.join(pages_dir, f"{name}.md")
    elif file_type == "journal":
        file_path = os.path.join(journals_dir, f"{name}.md")
    else:
        return jsonify({"error": f"Tipo inválido: '{file_type}'. Use 'page' ou 'journal'."}), 400

    # Verifica se o arquivo existe
    if not os.path.isfile(file_path):
        return jsonify({"error": f"O arquivo '{name}' não foi encontrado no tipo '{file_type}'."}), 404

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

