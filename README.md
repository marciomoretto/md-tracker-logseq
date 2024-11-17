<<<<<<< HEAD
O MD Tracker Logseq Plugin é uma ferramenta que amplia as funcionalidades do Logseq, permitindo que você explore facilmente os arquivos relacionados à página atual. Ele funciona em conjunto com o [MD Tracker](https://github.com/marciomoretto/md-tracker), que monitora pastas de arquivos Markdown e cria links RDF no Tracker3 para associar arquivos referenciados.

Com este plugin, basta um comando ou atalho no Logseq para abrir o GNOME Files (Nautilus) com todos os arquivos relacionados à página atual, direta ou indiretamente.

# Funcionalidade Principal
1. Como funciona:
 * No Logseq, pressione Ctrl+Shift+N ou digite o comando Nautilus no Command Palette.
 * O GNOME Files será aberto com uma pasta temporária contendo:
  * Arquivos diretamente citados na página atual.
  * Arquivos relacionados indiretamente por até dois níveis de referência.

# Instalação
1. Pré-requisitos
 1. MD Tracker:
  * Certifique-se de que o MD Tracker está instalado e funcionando.
  * Ele será responsável por criar os links RDF que este plugin utiliza.
 2. Dependências de Sistema:
  * Logseq instalado.
  * GNOME Files (Nautilus) como gerenciador de arquivos.
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
=======
# Logseq Nautilus Plugin

Um plugin para **Logseq** que integra funcionalidades de monitoramento, organização e sincronização de arquivos associados às páginas e journals no Logseq. Ele utiliza `inotify-tools`, **Tracker 3**, e um servidor Flask para gerenciar eventos e consultas relacionados a tags.

## **Funcionalidades Principais**

- 🔍 **Monitoramento Automático**: Observa mudanças em diretórios (`pages` e `journals`) e sincroniza tags automaticamente com o **Tracker 3**.
- 🌐 **Servidor Flask Integrado**: Processa requisições HTTP para manipulação e consulta de tags.
- 📂 **Organização Dinâmica**: Adiciona e remove tags automaticamente com base nos eventos detectados.
- ⚡ **Integração com Logseq**: Permite executar comandos diretamente no editor para consultar arquivos vinculados às páginas.

## **Requisitos**

- **Sistema Operacional:** Linux (suporte ao `inotify`).
- **Dependências do Sistema:** 
  - `inotify-tools`: Instale com:
    
    ```bash
    sudo apt install inotify-tools
    ```
  - **Python 3.8+**.
  - **Tracker 3** instalado e configurado.

## **Instalação**

1. Clone o Repositório:

   ```bash
   git clone https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
   cd SEU_REPOSITORIO
    ```

2. Configure e ative todos os serviços com o Makefile:

    ```bash
    make all
    ```

  Isso irá:

  * Criar e configurar o ambiente virtual.
  * Instalar as dependências do Python.
  * Configurar e ativar os serviços do monitoramento e do Flask.

## **Uso**

1. Monitoramento Automático

  O serviço de monitoramento observa os diretórios pages e journals e dispara eventos automaticamente quando detecta mudanças.

2. Comando no Logseq

  Ative o comando Nautilus no Logseq (ctrl+shift+n) para consultar arquivos vinculados à página atual.

3. Personalização do Diretório Base

  Se precisar alterar o diretório base para o monitoramento, use o comando:

  ```bash
  make BASE_DIR=/seu/caminho all
  ```

4. Logs
  * Logs do Flask:
  
  ```bash
  make logs
  ```

  * Logs do Monitoramento:

  ```bash
  make monitor_logs
  ```
>>>>>>> 03d0f96 (big bang)

