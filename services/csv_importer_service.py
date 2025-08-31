import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from repository.category_repository import list_categories
from repository.payment_repository import list_payments_by_user_id
from repository.transaction_repository import create_transection

from services.tools import real_coin_to_decimal, compare_texts

def prepare_params(file, user_id):
  categories = list_categories()
  payments = list_payments_by_user_id(user_id)

  df = pd.read_csv(file)

  new_payments = []

  db_session = Session()

  success = True

  message = None

  try:
    with db_session.begin():
      for _, row in df.iterrows():
        validate(row)

        expense = True if row['Despesa'] == 1 else False
        paid = True if row['Pago'] == 1 else False        
        date_at = datetime.strptime(row['Data'], '%d/%m/%Y')
        value = real_coin_to_decimal(row['Valor'])
        installments = int(row['Parcela Atual'])
        total_installments = int(row['Total de Parcelas'])

        category = next((category for category in categories if category.expense == expense and compare_texts(category.name, row['Categoria'])), None)
        payment = next((payment for payment in payments if compare_texts(payment.name, row['Tipo de Pagamento'])), None)

        payment_id = payment.id

        if int(row['Crédito']) == 1:
          payment_credit = next((payment for payment in payments if compare_texts(payment.name, row['Cartão'])), None)
          payment_id = payment_credit.id

        if category == None:
          category = next((category for category in categories if category.expense == expense and category.name == "Indefinido"), None)
      
        params = {
          'description': row['Descrição'],
          'value': value,
          'date_at': date_at,
          'expense': category.expense,
          'user_id': user_id,
          'category_id': category.id,
          'payment_id': payment_id,
          'paid_payment_id': payment.id,
          'payment_date': date_at,
          'paid': paid,
          'installments': installments,
          'total_installments': total_installments
        }

        new_payment = create_transection(params)
        new_payments.append(new_payment)
  except SQLAlchemyError as e:
    db_session.rollback()
    success = False
    message = f"Erro durante a transação: {e}"
  except Exception as e:
    db_session.rollback()
    success = False
    message = str(e)
  finally:
    db_session.close()

  return new_payments if success else message

def validate(row):
  if pd.isna(row['Tipo de Pagamento']):
    raise ValueError("O campo 'Tipo de Pagamento' está vazio (NaN)")

  if pd.isna(row['Categoria']):
    raise ValueError("O campo 'Categoria' está vazio (NaN)")
  
  if pd.isna(row['Descrição']):
    raise ValueError("O campo 'Descrição' está vazio (NaN)")

  if pd.isna(row['Data']):
    raise ValueError("O campo 'Data' está vazio (NaN)")

  if pd.isna(row['Parcela Atual']):
    raise ValueError("O campo 'Parcela Atual' está vazio (NaN)")

  if pd.isna(row['Total de Parcelas']):
    raise ValueError("O campo 'Total de Parcelas' está vazio (NaN)")
  
  if pd.isna(row['Crédito']):
    raise ValueError("O campo 'Crédito' está vazio (NaN)")

  if pd.isna(row['Pago']):
    raise ValueError("O campo 'Pago' está vazio (NaN)")

  if pd.isna(row['Despesa']):
    raise ValueError("O campo 'Despesa' está vazio (NaN)")

  if not isinstance(row['Parcela Atual'], int):
    raise ValueError("O valor do campo Crédito deve ser 1 ou 0")

  if not isinstance(row['Total de Parcelas'], int):
    raise ValueError("O valor do campo Crédito deve ser 1 ou 0")

  if not isinstance(row['Crédito'], int) or not row['Crédito'] in [0, 1]:
    raise ValueError("O valor do campo Crédito deve ser 1 ou 0")

  if not isinstance(row['Pago'], int) or not row['Pago'] in [0, 1]:
    raise ValueError("O valor do campo Crédito deve ser 1 ou 0")

  if not isinstance(row['Despesa'], int) or not row['Despesa'] in [0, 1]:
    raise ValueError("O valor do campo Crédito deve ser 1 ou 0")

  if row['Crédito'] == 1 and pd.isna(row['Cartão']):
    raise ValueError("O campo 'Cartão' está vazio (NaN)")
