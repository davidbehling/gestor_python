from database import session
from sqlalchemy import func, case, select, join, asc
from sqlalchemy.orm import aliased
from sqlalchemy.orm import joinedload

from models.category import Category
from models.payment import Payment
from models.transaction import Transaction
from models.user import User

def create_transection(params):
  transaction = Transaction(**params)
  session.add(transaction)
  session.commit()
  return transaction

def list_transactions(user_id):
    return session.query(Transaction).filter_by(user_id=user_id).all()

def list_transactions_values_expenses_to_categories(date_start=None, date_end=None, user_ids=None, category_ids=None, payment_ids=None):
  query = session.query(
      Category.name.label("category_name"),
      func.sum(Transaction.value).label("total_value")
  ).join(
      Transaction, Category.id == Transaction.category_id
  ).filter(
      Category.expense == True,
      Transaction.paid == True
  )
  
  if date_start and date_end:
      query = query.filter(Transaction.date_at.between(date_start, date_end))
  
  if user_ids:
      query = query.filter(Transaction.user_id.in_(user_ids))
  
  if category_ids:
      query = query.filter(Transaction.category_id.in_(category_ids))
  
  if payment_ids:
      query = query.filter(Transaction.paid_payment_id.in_(payment_ids))
  
  result = query.group_by(Category.name).all()
  return result


def total_expenses_and_incomes_values(date_start=None, date_end=None, user_ids=None, category_ids=None):
  expenses_query = session.query(
    func.sum(
      case((Transaction.paid == True, Transaction.value), else_=0)
    ).label("total_value")
  ).filter(Transaction.expense == True)

  incomes_query = session.query(
    func.sum(Transaction.value).label("total_value")
  ).filter(Transaction.expense == False)

  if date_start and date_end:
    expenses_query = expenses_query.filter(Transaction.date_at.between(date_start, date_end))
    incomes_query = incomes_query.filter(Transaction.date_at.between(date_start, date_end))
  if user_ids:
    expenses_query = expenses_query.filter(Transaction.user_id.in_(user_ids))
    incomes_query = incomes_query.filter(Transaction.user_id.in_(user_ids))
  
  if category_ids:
    expenses_query = expenses_query.filter(Transaction.category_id.in_(category_ids))

  total_expenses = expenses_query.scalar() or 0
  total_incomes = incomes_query.scalar() or 0

  objects = [
      {"expense": True, "value": total_expenses},
      {"expense": False, "value": total_incomes}
  ]

  return objects

def list_transactions_details(expense=None, date_start=None, date_end=None, user_ids=None, category_ids=None, payment_ids=None, paid=None):
  CategoryAlias = aliased(Category)
  PaymentAlias = aliased(Payment)
  UserAlias = aliased(User)

  stmt = (
    select(
      Transaction.id.label("id"),
      Transaction.description.label("description"),
      Transaction.value.label("value"),
      Transaction.date_at.label("date_at"),
      Transaction.due_date.label("due_date"),
      Transaction.payment_date.label("payment_date"),
      Transaction.installments.label("installments"),
      Transaction.total_installments.label("total_installments"),
      Transaction.paid.label("paid"),
      Transaction.expense.label("expense"),
      CategoryAlias.id.label("category_id"),
      CategoryAlias.name.label("category_name"),
      PaymentAlias.id.label("payment_id"),
      PaymentAlias.type.label("payment_type"),
      PaymentAlias.name.label("payment_name"),
      UserAlias.id.label("user_id"),
      UserAlias.name.label("user_name"),
    )
    .join(CategoryAlias, CategoryAlias.id == Transaction.category_id, isouter=True)
    .join(PaymentAlias, PaymentAlias.id == Transaction.payment_id, isouter=True)
    .join(UserAlias, UserAlias.id == Transaction.user_id, isouter=True)
    .order_by(Transaction.payment_date)
  )

  if expense != None:
    stmt = stmt.filter(Transaction.expense == expense)
  
  if paid != None:
    stmt = stmt.filter(Transaction.paid == paid)

  if date_start and date_end:
    stmt = stmt.filter(Transaction.payment_date.between(date_start, date_end))
  
  if user_ids:
    stmt = stmt.filter(Transaction.user_id.in_(user_ids))
  
  if category_ids:
    stmt = stmt.filter(Transaction.category_id.in_(category_ids))
  
  if payment_ids:
    stmt = stmt.filter(Transaction.payment_id.in_(payment_ids))

  results = session.execute(stmt).fetchall()
  return results

def find_transaction_id(id):
  return session.query(Transaction).filter_by(id=id).first()

def update_transaction(id, description, value, date_at, user_id, category_id, payment_id, total_installments=None):
  transaction = find_transaction_id(id)
  transaction.description = description
  transaction.value = value
  transaction.date_at = date_at
  transaction.user_id = user_id
  transaction.category_id = category_id
  transaction.payment_id = payment_id

  if total_installments:
    transaction.total_installments = total_installments
      
  session.commit()

def delete_transaction(id):
  transaction = find_transaction_id(id)
  session.delete(transaction)
  session.commit()

def confirm_pay(id, payment_id):
  transaction = find_transaction_id(id)
  transaction.paid = True
  transaction.paid_payment_id = payment_id
  session.commit()

def export_transaction(user_ids):
  CategoryAlias = aliased(Category)
  PaymentAlias = aliased(Payment)
  PaymentAliasPaid = aliased(Payment)

  stmt = (
    select(
      Transaction.id.label("id"),
      PaymentAlias.name.label("payment_name"),                    # Tipo de Pagamento
      CategoryAlias.name.label("category_name"),                  # Categoria
      Transaction.value.label("value"),                           # Valor
      Transaction.description.label("description"),               # Descrição
      Transaction.date_at.label("payment_date"),                  # Data
      Transaction.installments.label("installments"),             # Parcela Atual
      Transaction.total_installments.label("total_installments"), # Total de Parcelas
      PaymentAlias.type.label("payment_type"),                    # Crédito
      PaymentAlias.name.label("payment_name"),                    # Cartão
      PaymentAliasPaid.type.label("payment_paid_type"),           # Crédito
      PaymentAliasPaid.name.label("payment_paid_name"),           # Cartão
      Transaction.paid.label("paid"),                             # Pago      
      Transaction.expense.label("expense"),                       # Despesa
      Transaction.due_date.label("due_date"),
      Transaction.payment_date.label("date_at")
    )
    .join(CategoryAlias, CategoryAlias.id == Transaction.category_id, isouter=True)
    .join(PaymentAlias, PaymentAlias.id == Transaction.payment_id, isouter=True)
    .join(PaymentAliasPaid, PaymentAliasPaid.id == Transaction.paid_payment_id, isouter=True)
    .order_by(Transaction.payment_date)
  )

  stmt = stmt.filter(Transaction.user_id.in_(user_ids))

  results = session.execute(stmt).fetchall()

  return results