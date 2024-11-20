# MD Tracker LogSeq Plugin

O MD Tracker Logseq Plugin é uma ferramenta que amplia as funcionalidades do Logseq, permitindo que você explore facilmente os arquivos relacionados à página atual. Ele funciona em conjunto com o [MD Tracker](https://github.com/marciomoretto/md-tracker), que monitora pastas de arquivos Markdown e cria links RDF no Tracker3 para associar arquivos referenciados.

Com este plugin, basta um comando ou atalho no Logseq para abrir o gerenciador padrão de arquivos com todos os arquivos relacionados à página atual, direta ou indiretamente.

# Funcionalidade Principal
1. Como funciona:
 * No Logseq, pressione Ctrl+Shift+N ou digite o comando Nautilus no Command Palette.
 * O gerenciador padrão de arquivos será aberto com uma pasta temporária contendo:
  * Arquivos diretamente citados na página atual.
  * Arquivos relacionados indiretamente por até dois níveis de referência.

# Instalação
1. Pré-requisitos
 1. MD Tracker:
  * Certifique-se de que o MD Tracker está instalado e funcionando.
  * Ele será responsável por criar os links RDF que este plugin utiliza.
 2. Dependências de Sistema:
  * Logseq instalado.
  * Tracker3 configurado no sistema.
2. Instale o Plugin
Clone este repositório e execute o comando abaixo para configurar automaticamente o ambiente:
```bash
git clone https://github.com/seu-usuario/logseq-plugin.git
cd logseq-plugin
make all
```
Este comando:
* Instala o plugin no Logseq (~/.logseq/plugins/).
* Configura um servidor Flask para processar as buscas.
* Habilita o servidor como um serviço no systemd.

3. Certifique-se de que o arquivo de configuração possui os caminhas para as pastas ou edite-o:
  ```bash
  sudo nano /etc/md-tracker/config
  ```
  * Exemplo:
    ```bash
    PAGES_DIR="/home/user/Documentos/Vault/pages"
    JOURNALS_DIR="/home/user/Documentos/Vault/journals"
    ```

# Uso
1. No Logseq:
 * Navegue até a página Markdown desejada.
 * Pressione Ctrl+Shift+N ou digite o comando Nautilus no Command Palette.
2. Explorar Arquivos:
 * O GNOME Files será aberto com uma pasta temporária contendo os arquivos relacionados à página atual, organizados para fácil navegação.

# Desinstalação
Para remover o plugin e o servidor Flask, execute:

```bash
make uninstall
```

# Licença
Este projeto é licenciado sob a GPL 3.0.
