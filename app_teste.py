import csv
import os
import tkinter as tk
from tkinter import filedialog

def export_to_csv(filepath, data, headers=None):
    """
    Exporta os dados para um arquivo CSV no local escolhido pelo usuário.

    :param filepath: Caminho completo do arquivo CSV.
    :param data: Lista de dicionários contendo os dados a serem exportados.
    :param headers: Lista opcional de cabeçalhos para o CSV.
    """
    directory = os.path.dirname(filepath)
    os.makedirs(directory, exist_ok=True)  # Garante que o diretório existe

    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        if not headers and data:
            headers = data[0].keys()

        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

    print(f"Arquivo '{filepath}' exportado com sucesso!")

def select_directory_and_export():
    """
    Abre um modal para selecionar o local e o nome do arquivo CSV a ser salvo.
    """
    root = tk.Tk()
    root.withdraw()  # Oculta a janela principal do Tkinter

    filepath = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Escolha onde salvar o arquivo",
        initialfile="dados.csv"
    )

    if filepath:  # Se o usuário não cancelar
        export_to_csv(filepath, data)

# Exemplo de dados
data = [
    {"Nome": "Alice", "Idade": 25, "Cidade": "São Paulo"},
    {"Nome": "Bruno", "Idade": 30, "Cidade": "Rio de Janeiro"},
    {"Nome": "Carlos", "Idade": 22, "Cidade": "Belo Horizonte"}
]

# Simulando o clique no botão chamando a função
select_directory_and_export()
