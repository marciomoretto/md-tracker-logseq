# Variáveis Gerais
SRC_DIR=src
REQUIREMENTS=$(SRC_DIR)/requirements.txt

# Monitoramento de Arquivos
MONITOR_SCRIPT=$(SRC_DIR)/monitor_vault.sh
PYTHON_SCRIPT=$(SRC_DIR)/tracker_logseq.py
MONITOR_SERVICE_FILE=$(SRC_DIR)/monitor.service
SYSTEMD_DIR=/etc/systemd/system
BASE_DIR ?= $(HOME)/Documentos/Vault

# Servidor Flask
FLASK_SCRIPT=$(SRC_DIR)/flask_server.py
START_FLASK_SCRIPT=$(SRC_DIR)/start_flask.sh
FLASK_SERVICE_FILE=$(SRC_DIR)/flask_service.service
USER_SYSTEMD_DIR=$(HOME)/.config/systemd/user

# Ambiente Virtual
ENV_DIR=$(SRC_DIR)/env

# Alvos
.PHONY: all setup monitor_service flask_service logs monitor_logs clean

# Configura tudo
all: setup monitor_service flask_service

# Configura o ambiente
setup: create_env install_dependencies
	@echo "Configurando o ambiente geral..."
	# Verifica se inotify-tools está instalado
	@if ! command -v inotifywait &> /dev/null; then \
	  echo "inotify-tools não está instalado. Instale com: sudo apt install inotify-tools"; \
	  exit 1; \
	fi
	# Verifica se os diretórios necessários existem
	@if [ ! -d "$(BASE_DIR)/pages" ] || [ ! -d "$(BASE_DIR)/journals" ]; then \
	  echo "Diretórios 'pages' e 'journals' não encontrados em $(BASE_DIR)."; \
	  exit 1; \
	fi
	# Verifica se os scripts do monitoramento existem
	@if [ ! -f "$(MONITOR_SCRIPT)" ]; then \
	  echo "O script '$(MONITOR_SCRIPT)' não foi encontrado."; \
	  exit 1; \
	fi
	@if [ ! -f "$(PYTHON_SCRIPT)" ]; then \
	  echo "O script '$(PYTHON_SCRIPT)' não foi encontrado."; \
	  exit 1; \
	fi
	# Verifica se os scripts do servidor Flask existem
	@if [ ! -f "$(FLASK_SCRIPT)" ]; then \
	  echo "O script Flask '$(FLASK_SCRIPT)' não foi encontrado."; \
	  exit 1; \
	fi
	@if [ ! -f "$(START_FLASK_SCRIPT)" ]; then \
	  echo "O script '$(START_FLASK_SCRIPT)' não foi encontrado."; \
	  exit 1; \
	fi
	# Configura permissões para os scripts
	chmod +x $(MONITOR_SCRIPT)
	chmod +x $(PYTHON_SCRIPT)
	chmod +x $(START_FLASK_SCRIPT)

# Cria o ambiente virtual
create_env:
	@echo "Criando ambiente virtual..."
	@if [ ! -d "$(ENV_DIR)" ]; then \
	  python3 -m venv $(ENV_DIR); \
	fi

# Instala dependências dentro do ambiente virtual
install_dependencies: create_env
	@echo "Instalando dependências no ambiente virtual..."
	source $(ENV_DIR)/bin/activate && pip install -r $(REQUIREMENTS)

# Configura o serviço do monitoramento
monitor_service:
	@echo "Instalando o serviço 'monitor.service' no systemd..."
	# Copia o arquivo de serviço para o systemd
	sudo cp $(MONITOR_SERVICE_FILE) $(SYSTEMD_DIR)/monitor.service
	# Recarrega as configurações do systemd
	sudo systemctl daemon-reload
	# Ativa o serviço para inicialização no boot
	sudo systemctl enable monitor.service
	@echo "Serviço 'monitor.service' instalado e ativado."

# Configura o serviço Flask
flask_service:
	@echo "Instalando o serviço 'flask_service.service' no systemd do usuário..."
	# Copia o arquivo de serviço para o diretório systemd do usuário
	mkdir -p $(USER_SYSTEMD_DIR)
	cp $(FLASK_SERVICE_FILE) $(USER_SYSTEMD_DIR)/flask_service.service
	# Recarrega as configurações do systemd
	systemctl --user daemon-reload
	# Ativa o serviço para inicialização no boot
	systemctl --user enable flask_service.service
	@echo "Serviço 'flask_service.service' instalado e ativado."

# Logs do Flask
logs:
	@echo "Exibindo logs do serviço Flask..."
	journalctl --user -u flask_service.service -f

# Logs do Monitoramento
monitor_logs:
	@echo "Exibindo logs do serviço de monitoramento..."
	sudo journalctl -u monitor.service -f

# Limpa o ambiente
clean:
	@echo "Limpando configurações..."
	rm -rf $(ENV_DIR)
	rm -f *.pyc
	rm -rf __pycache__
	# Para e remove o serviço do monitoramento
	sudo systemctl stop monitor.service || true
	sudo systemctl disable monitor.service || true
	sudo rm -f $(SYSTEMD_DIR)/monitor.service
	# Para e remove o serviço Flask
	systemctl --user stop flask_service.service || true
	systemctl --user disable flask_service.service || true
	rm -f $(USER_SYSTEMD_DIR)/flask_service.service
	# Recarrega o systemd
	sudo systemctl daemon-reload
	systemctl --user daemon-reload
	@echo "Serviços removidos e ambiente limpo."

