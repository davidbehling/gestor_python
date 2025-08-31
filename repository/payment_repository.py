from database import session
from sqlalchemy.orm import aliased
from sqlalchemy import select, join, asc
from sqlalchemy.orm import joinedload

from models.payment import Payment
from models.bank_account import BankAccount
from models.user import User


def create_payment(name, payment_type, user_id, bank_account_id=None, due_day=None, closed_day=None):
    payment = Payment(
        name=name,
        type=payment_type,
        user_id=user_id,
        bank_account_id=bank_account_id,
        due_day=due_day,
        closed_day=closed_day
    )
    session.add(payment)
    session.commit()
    return payment

def list_payments(user_ids=None, bank_account_ids=None, payment_type=None):
    UserAlias = aliased(User)
    BankAccountAlias = aliased(BankAccount)

    stmt = (
        select(
            Payment.id.label("id"),
            Payment.name.label("name"),
            Payment.type.label("type"),
            Payment.due_day.label("due_day"),
            Payment.closed_day.label("closed_day"),
            UserAlias.id.label("user_id"),
            UserAlias.name.label("user_name"),
            BankAccountAlias.id.label("bank_account_id"),
            BankAccountAlias.name.label("bank_account_name"),
        )
        .join(BankAccountAlias, BankAccountAlias.id == Payment.bank_account_id, isouter=True)
        .join(UserAlias, UserAlias.id == Payment.user_id, isouter=True)
        .order_by(UserAlias.name, Payment.name)
    )

    if user_ids:
        stmt = stmt.filter(UserAlias.id.in_(user_ids)) 
    if bank_account_ids:
        stmt = stmt.filter(Payment.bank_account_id.in_(bank_account_ids))
    if payment_type:
        stmt = stmt.filter(Payment.type.in_(payment_type))

    results = session.execute(stmt).fetchall()
    return results

def list_payments_by_user_id(user_id):
    return session.query(Payment).filter_by(user_id=user_id).order_by(Payment.name.asc()).all()

def list_payments_by_bank_account_id(bank_account_id):
    return session.query(Payment).filter_by(bank_account_id=bank_account_id).order_by(Payment.name.asc()).all()

def find_payment_id(id):
    return session.query(Payment).filter_by(id=id).first()

def delete_payments_by_user_id(user_id):
    session.query(Payment).filter(Payment.user_id == user_id).delete(synchronize_session=False)
    session.commit()

def delete_payments_by_bank_account_id(user_id):
    session.query(Payment).filter(Payment.bank_account_id == bank_account_id).delete(synchronize_session=False)
    session.commit()

def find_payment_id(id):
    return session.query(Payment).filter_by(id=id).first()

def update_payment(id, new_name, closed_day=None, due_day=None):
    payment = find_payment_id(id)
    payment.name = new_name

    if closed_day:
      payment.closed_day = closed_day

    if due_day:
      payment.due_day = due_day

    session.commit()

def delete_payment(id):
    payment = find_payment_id(id)
    session.delete(payment)
    session.commit()
