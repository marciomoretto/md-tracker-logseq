#!/bin/bash

# Inicializa variáveis
PAGES=""
JOURNALS=""

# Função para exibir a mensagem de uso
function usage() {
  echo "Uso: $0 -pages PATH_TO_PAGES -journals PATH_TO_JOURNALS"
  echo "  -pages     Caminho para o diretório de páginas (obrigatório)"
  echo "  -journals  Caminho para o diretório de journals (obrigatório)"
  exit 1
}

# Processa os argumentos da linha de comando
while [[ "$#" -gt 0 ]]; do
  case $1 in
    -pages)
      PAGES="$2"
      shift 2
      ;;
    -journals)
      JOURNALS="$2"
      shift 2
      ;;
    *)
      echo "Erro: Argumento desconhecido: $1"
      usage
      ;;
  esac
done

# Verifica se ambos os argumentos foram fornecidos
if [[ -z "$PAGES" || -z "$JOURNALS" ]]; then
  echo "Erro: Ambos os argumentos -pages e -journals são obrigatórios."
  usage
fi

# Verifica se os diretórios fornecidos existem
if [[ ! -d "$PAGES" ]]; then
  echo "Erro: O diretório de páginas ($PAGES) não existe."
  exit 1
fi

if [[ ! -d "$JOURNALS" ]]; then
  echo "Erro: O diretório de journals ($JOURNALS) não existe."
  exit 1
fi

# Executa o script Python com os diretórios fornecidos
$HOME/.logseq/plugins/md-tracker-logseq/server/venv/bin/python3 \
  $HOME/.logseq/plugins/md-tracker-logseq/server/flask_server.py \
  "$PAGES" "$JOURNALS"
