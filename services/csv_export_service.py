import csv
import os
import tkinter as tk
from tkinter import filedialog

from repository.transaction_repository import export_transaction
from services.tools import to_string_date_br, to_money

def header():
  data = [
    "Tipo de Pagamento",
    "Categoria",
    "Valor",
    "Descrição",
    "Data",
    "Parcela Atual",
    "Total de Parcelas",
    "Crédito",
    "Cartão",
    "Pago",
    "Despesa"
  ]  
  return data

def modelo():
  data = [
    { 
      "Tipo de Pagamento": "DEBITO", 
      "Categoria": "Pagamento", 
      "Valor": "R$3.500,00", 
      "Descrição": "Pagamento", 
      "Data": "01/02/2025", 
      "Parcela Atual": 1, 
      "Total de Parcelas": 1, 
      "Crédito": 0, 
      "Cartão": "", 
      "Pago": 1, 
      "Despesa": 0 
    },
    { 
      "Tipo de Pagamento": "DEBITO", 
      "Categoria": "Mercado", 
      "Valor": "R$100,00", 
      "Descrição": "Feijão", 
      "Data": "02/02/2025", 
      "Parcela Atual": 1, 
      "Total de Parcelas": 1, 
      "Crédito": 0, 
      "Cartão": "", 
      "Pago": 1, 
      "Despesa": 1 
    },
    { 
      "Tipo de Pagamento": "DEBITO", 
      "Categoria": "Padaria",
      "Valor": "R$25,00", 
      "Descrição": "Bolo", 
      "Data": "03/02/2025", 
      "Parcela Atual": 1, 
      "Total de Parcelas": 1, 
      "Crédito": 0, 
      "Cartão": "", 
      "Pago": 1, 
      "Despesa": 1 
    },
    { 
      "Tipo de Pagamento": "DEBITO", 
      "Categoria": "Eletrodomestico", 
      "Valor": "R$1.000,00", 
      "Descrição": "Tv 40 Led", 
      "Data": "04/02/2025", 
      "Parcela Atual": 1, 
      "Total de Parcelas": 2, 
      "Crédito": 1, "Cartão": 
      "Ponto Frio", "Pago": 1,
       "Despesa": 1 
    },
    { 
      "Tipo de Pagamento": "Ponto Frio", 
      "Categoria": "Eletrodomestico", 
      "Valor": "R$1.000,00", 
      "Descrição": "Tv 40 Led",
      "Data": "04/02/2025", 
      "Parcela Atual": 1, 
      "Total de Parcelas": 2, 
      "Crédito": 1, 
      "Cartão": "Ponto Frio", 
      "Pago": 0,
      "Despesa": 1
    }    
  ]
  return data

def model_export():
  select_directory_and_export(modelo(), headers=header())

def transactions_export(user_id):
  #import pdb; pdb.set_trace()
  transactions = export_transaction([user_id])

  data = [
    { 
      "Tipo de Pagamento": transaction.payment_paid_name, 
      "Categoria": transaction.category_name, 
      "Valor": to_money(transaction.value), 
      "Descrição": transaction.description, 
      "Data": to_string_date_br(transaction.payment_date), 
      "Parcela Atual": transaction.installments, 
      "Total de Parcelas": transaction.total_installments, 
      "Crédito": 0 if transaction.payment_type in ['Débito', 'Dinheiro'] else 1, 
      "Cartão": None if transaction.payment_type in ['Débito', 'Dinheiro'] else transaction.payment_name, 
      "Pago": 1 if transaction.paid else 0, 
      "Despesa": 1 if transaction.expense else 0
    } for transaction in transactions
  ]

  select_directory_and_export(data, headers=header())

def export_to_csv(filepath, data, headers=None):
  directory = os.path.dirname(filepath)
  os.makedirs(directory, exist_ok=True)

  with open(filepath, mode='w', newline='', encoding='utf-8') as file:
    if not headers and data:
        headers = data[0].keys()

    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    writer.writerows(data)

  
  print(f"Arquivo '{filepath}' exportado com sucesso!")

def select_directory_and_export(data, headers=None):
  filepath = filedialog.asksaveasfilename(
      defaultextension=".csv",
      filetypes=[("CSV files", "*.csv")],
      title="Escolha onde salvar o arquivo",
      initialfile="dados.csv"
  )

  if filepath:
    export_to_csv(filepath, data, headers)
