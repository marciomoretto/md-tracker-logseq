#!/bin/bash

# Carregar o arquivo de configuração e suas variáveis
source $HOME/.config/md-watcher/config

# Verificar se a variável MONITORED_DIRS está definida
if [ -z "$MONITORED_DIRS" ]; then
  echo "Erro: A variável MONITORED_DIRS não está definida no arquivo de configuração."
  exit 1
fi

$HOME/.logseq/plugins/md-tracker-logseq/server/venv/bin/python3 $HOME/.logseq/plugins/md-tracker-logseq/server/flask_server.py $MONITORED_DIRS
