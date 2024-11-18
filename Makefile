# Diretórios e arquivos
PLUGIN_DIR = ~/.logseq/plugins/logseq-plugin
SERVER_DIR = server
ENV_DIR = $(SERVER_DIR)/env

FLASK_SERVICE = $(SERVER_DIR)/flask_service.service
START_FLASK = $(SERVER_DIR)/start_flask.sh

# Alvos principais
.PHONY: all install-plugin install-server enable-service uninstall clean

# Instalação completa
all: install-plugin install-server enable-service

# Instalar o plugin no Logseq
install-plugin:
	@echo "Instalando o plugin no Logseq..."
	mkdir -p $(PLUGIN_DIR)
	cp index.js index.html logseq.png package.json tsconfig.json $(PLUGIN_DIR)/
	@echo "Plugin instalado com sucesso em $(PLUGIN_DIR)!"

# Configurar o servidor Flask
install-server:
	@echo "Copiando o ambiente Python pré-configurado..."
	mkdir -p ~/.config/systemd/user/
	cp -r $(SERVER_DIR) ~/.config/systemd/user/
	chmod +x ~/.config/systemd/user/$(START_FLASK)
	@echo "Configurando o serviço do Flask..."
	cp $(FLASK_SERVICE) ~/.config/systemd/user/
	systemctl --user daemon-reload
	@echo "Servidor Flask configurado com sucesso!"

# Habilitar o serviço do Flask na inicialização
enable-service:
	@echo "Habilitando o serviço do Flask na inicialização..."
	systemctl --user enable flask_service.service
	@echo "Serviço habilitado com sucesso!"

# Desinstalar o projeto
uninstall:
	@echo "Desinstalando o plugin do Logseq..."
	rm -rf $(PLUGIN_DIR)
	@echo "Parando e removendo o servidor Flask..."
	systemctl --user stop flask_service.service || true
	systemctl --user disable flask_service.service || true
	rm -f ~/.config/systemd/user/flask_service.service
	rm -rf ~/.config/systemd/user/$(SERVER_DIR)
	systemctl --user daemon-reload
	@echo "Projeto desinstalado com sucesso!"

# Limpar arquivos temporários
clean:
	@echo "Limpando arquivos temporários..."
	rm -rf ~/.config/systemd/user/$(SERVER_DIR)
	rm -f ~/.config/systemd/user/flask_service.service
	@echo "Limpeza concluída!"




