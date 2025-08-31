from datetime import datetime
from dateutil.relativedelta import relativedelta

from repository.category_repository import find_category_id
from repository.payment_repository import find_payment_id
from repository.transaction_repository import create_transection

def create_transaction_serv(description, value, date_at, user_id, category_id, payment_id, total_installments=None):
  
  category = find_category_id(category_id)

  expense = category.expense     
  
  params = {
    'description': description,
    'value': value,
    'date_at': datetime.strptime(date_at, '%Y-%m-%d'),
    'expense': expense,
    'user_id': user_id,
    'category_id': category_id,
    'payment_id': payment_id,
    'paid_payment_id': payment_id,
    'payment_date': datetime.strptime(date_at, '%Y-%m-%d'),
    'paid': True
  }

  payment = find_payment_id(payment_id)

  if total_installments not in [None, 0] and payment.closed_day not in [None, 0]:    
    params['paid'] = False
    params['value'] = value / total_installments
    params['total_installments'] = total_installments
    params['installments'] = 0

    due_dates = due_dates_generate(total_installments, date_at, payment.due_day, payment.closed_day)

    new_payments = []

    for due_date in due_dates:
      params['due_date'] = due_date
      params['payment_date'] = due_date
      params['installments'] += 1
      new_payment = create_transection(params)
      new_payments.append(new_payment)
    
    return new_payments
  else:
    return create_transection(params)

def due_dates_generate(total_installments, date_at, due_day, closed_day):
  purchase_data = datetime.strptime(date_at, '%Y-%m-%d')

  due_dates = []

  for i in range(total_installments):
    due_date_calculated = None

    if not due_dates:
      due_date_calculated = purchase_data.replace(day=due_day)

      if purchase_data.day > closed_day:
          due_date_calculated += relativedelta(months=1)
    else:
      due_date_calculated = due_dates[-1] + relativedelta(months=1)
    
    due_dates.append(due_date_calculated)

  return due_dates

def export_transactions():
  return
