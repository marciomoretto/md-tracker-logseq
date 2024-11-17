#!/usr/bin/python3

import os
import re
import sys
import urllib.parse
import subprocess
import tempfile
from pathlib import Path
import time
import argparse

def show_help():
    print("Uso: python script.py FILE_PATH")
    print("\nBusca arquivos associados a uma tag específica no Tracker e exibe-os em uma pasta temporária no Nautilus.")
    print("\nArgumentos:")
    print("  FILE_PATH          Caminho para o arquivo.")
    print("\nExemplo de uso:")
    print("  python script.py '~/Documentos/Vault/pages/O Justo - Ricoeur.md'")
    sys.exit()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Script para buscar arquivos linkados no Tracker.")
    parser.add_argument("link", nargs="?", help="Caminho para o arquivo.")
    parser.add_argument("--list-relations", action="store_true", help="Lista todas as relações entre arquivos e tags.")

    return parser.parse_args()

def urlencode(text):
    return urllib.parse.quote(text, safe='')

def urldecode(text):
    return urllib.parse.unquote(text)

def list_file_links():
    """
    Lista os links RDF entre arquivos usando a propriedade nie:links.
    """
    try:
        # Executa a consulta SPARQL para buscar links entre arquivos
        result = subprocess.run(
            ["tracker3", "sparql", "--dbus-service=org.freedesktop.Tracker3.Miner.Files",
             "-q", "SELECT ?file1 ?file2 WHERE { ?file1 nie:relatedTo ?file2 }"],
            stdout=subprocess.PIPE, text=True, check=True
        )
        # Parse o resultado da consulta SPARQL
        links = re.findall(r'file://[^\s]+', result.stdout)
        parsed_links = []

        # Itera a cada 2 elementos para garantir pares completos (file1 -> file2)
        for i in range(0, len(links), 2):
            if i + 1 < len(links):  # Verifica se há um par completo
                file1_uri = links[i]
                file2_uri = links[i + 1]
                file1_path = urllib.parse.unquote(file1_uri.replace("file://", ""))
                file2_path = urllib.parse.unquote(file2_uri.replace("file://", ""))
                parsed_links.append((file1_path, file2_path))
            else:
                print(f"Aviso: Par incompleto encontrado na posição {i}. Ignorando...")

        return parsed_links
    except subprocess.CalledProcessError as e:
        print("Erro ao executar a consulta SPARQL para listar links entre arquivos:", e)
        return []

def search_files_by_link(link):
    encoded_link = "file://" + urlencode(link)
    print(f"tracker3 sparql --dbus-service=org.freedesktop.Tracker3.Miner.Files -q SELECT ?file WHERE {{ ?file nie:relatedTo '{encoded_link}' }}")
    try:
        result = subprocess.run(
            ["tracker3", "sparql", "--dbus-service=org.freedesktop.Tracker3.Miner.Files",
             "-q", f"SELECT ?file WHERE {{ ?file nie:relatedTo '{encoded_link}' }}"],
            stdout=subprocess.PIPE, text=True, check=True
        )
        print(result)
        return re.findall(r'file://.*', result.stdout)
    except subprocess.CalledProcessError as e:
        print("Erro ao executar a consulta SPARQL:", e)
        return []

def search_files_two_hops(link):
    """
    Busca arquivos relacionados ao nó inicial em até dois passos no grafo RDF.
    Retorna dois conjuntos: arquivos a 1 passo e arquivos a 2 passos.
    """
    encoded_link = "file://" + urlencode(link)

    # Consulta para o primeiro nível (1 passo)
    query_first_hop = f"""
    SELECT ?file1 WHERE {{
        <{encoded_link}> nie:relatedTo ?file1 .
    }}
    """

    # Consulta para o segundo nível (2 passos)
    query_second_hop = f"""
    SELECT ?file2 WHERE {{
        <{encoded_link}> nie:relatedTo ?intermediate .
        ?intermediate nie:relatedTo ?file2 .
    }}
    """

    try:
        # Busca arquivos a 1 passo
        result_first_hop = subprocess.run(
            ["tracker3", "sparql", "--dbus-service=org.freedesktop.Tracker3.Miner.Files",
             "-q", query_first_hop],
            stdout=subprocess.PIPE, text=True, check=True
        )
        files_first_hop = re.findall(r'file://[^\s]+', result_first_hop.stdout)

        # Busca arquivos a 2 passos
        result_second_hop = subprocess.run(
            ["tracker3", "sparql", "--dbus-service=org.freedesktop.Tracker3.Miner.Files",
             "-q", query_second_hop],
            stdout=subprocess.PIPE, text=True, check=True
        )
        files_second_hop = re.findall(r'file://[^\s]+', result_second_hop.stdout)

        return (
            {urllib.parse.unquote(uri.replace("file://", "")) for uri in files_first_hop},
            {urllib.parse.unquote(uri.replace("file://", "")) for uri in files_second_hop},
        )
    except subprocess.CalledProcessError as e:
        print("Erro ao executar a consulta SPARQL:", e)
        return set(), set()

def create_links_with_hops(file_uris, temp_dir):
    """
    Cria links simbólicos na pasta temporária para os arquivos encontrados.
    Inclui uma indicação do nível do passo no nome do link simbólico.
    """
    for file_path in file_uris:
        print(f"URI do arquivo: {file_path}")

        if not os.path.exists(file_path):
            print(f"Aviso: Arquivo não encontrado - {file_path}")
            continue

        # Ignora arquivos com extensão .md
        if file_path.endswith(".md"):
            print(f"Ignorando arquivo com extensão .md: {file_path}")
            continue

        basename = os.path.basename(file_path)
        link_path = os.path.join(temp_dir, basename)

        # Verifica se o link já existe e pula a criação se já estiver presente
        if os.path.exists(link_path):
            print(f"Link simbólico já existe: {link_path}")
        else:
            print(f"Criando link simbólico para: {file_path} -> {link_path}")
            os.symlink(file_path, link_path)

def create_links(file_uris, temp_dir):
    for file_uri in file_uris:
        file_path = urllib.parse.unquote(file_uri.replace("file://", ""))
        print(f"URI original do arquivo: {file_uri}")
        print(f"Caminho decodificado do arquivo: {file_path}")

        # Ignora arquivos com extensão .md
        if file_path.endswith(".md"):
            print(f"Ignorando arquivo com extensão .md: {file_path}")
            continue

        if not os.path.exists(file_path):
            print(f"Aviso: Arquivo não encontrado - {file_path}")
            continue

        basename = os.path.basename(file_path)
        link_path = os.path.join(temp_dir, basename)

        # Verifica se o link já existe e pula a criação se já estiver presente
        if os.path.exists(link_path):
            print(f"Link simbólico já existe: {link_path}")
        else:
            print(f"Criando link simbólico para: {file_path} -> {link_path}")
            os.symlink(file_path, link_path)

def main():
    args = parse_arguments()
    link = args.link

    if args.list_relations:
        print("Listando todas as relações entre arquivos:")
        relations = list_file_links()
        if relations:
            print(f"{'Arquivo 1':<50} | {'Arquivo 2'}")
            print(f"{'-'*50} | {'-'*50}")
            for file1_path, file2_path in relations:
                print(f"{file1_path:<50} | {file2_path:<50}")
        else:
            print("Nenhuma relação encontrada entre arquivos.")
        sys.exit()

    if not link:
        print("Erro: Caminho para o arquivo não fornecido.")
        sys.exit(1)

    temp_dir = tempfile.mkdtemp(prefix="link_search_")
    print(f"Pasta temporária criada para links simbólicos: {temp_dir}")

    print(f"Executando consulta SPARQL para dois níveis de hops a partir de '{link}'")
    files_one_hop, files_two_hop = search_files_two_hops(link)

    print("\nArquivos a 1 passo:")
    print("\n".join(files_one_hop))
    print("\nArquivos a 2 passos:")
    print("\n".join(files_two_hop))

    # Cria links simbólicos para arquivos a 1 e 2 passos
    create_links_with_hops(files_one_hop, temp_dir)
    create_links_with_hops(files_two_hop, temp_dir)

    time.sleep(1)
    print("Conteúdo do diretório temporário antes de abrir no Nautilus:")
    subprocess.run(["ls", "-l", temp_dir])

    if any(Path(temp_dir).iterdir()):
        print(f"Abrindo pasta temporária no Nautilus: {temp_dir}")
        subprocess.run(["nautilus", temp_dir])
        time.sleep(5)  # Ajuste ou remova conforme necessário
    else:
        print(f"Nenhum arquivo encontrado. Removendo pasta temporária.")

if __name__ == "__main__":
    main()